import pprint
import logging
import asyncio
from itertools import chain
from playwright.async_api import async_playwright

from .scrappers import PikabuScrapper, NineGagScrapper, JoyreactorScrapper
from .collection import PostsFilter, MediaDownloader, PostsCategorizer
from src.database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


async def _init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    logger.info("Playwright had been start")
    logger.info("Browser had been created")
    return playwright, browser


async def _close_browser(playwright, browser):
    await browser.close()
    await playwright.stop()
    logger.info("Browser had been closed")
    logger.info("Playwright had been stop")


def make_pools_chain(platforms_tasks: list[list[asyncio.Task]]):
    max_platform_tasks_chain = 0
    for platform_tasks in platforms_tasks:
        max_platform_tasks_chain = max(max_platform_tasks_chain, len(platform_tasks))

    new_platforms_tasks = list()
    for platform_tasks in platforms_tasks:
        tasks = platform_tasks
        while len(platform_tasks) < max_platform_tasks_chain:
            tasks.append(None)
        new_platforms_tasks.append(tasks)

    # transplant the matrix
    pools_chain = [[None] * max_platform_tasks_chain for _ in range(max_platform_tasks_chain)]
    for m, new_platform_tasks in enumerate(new_platforms_tasks):
        for n, new_platform_task in enumerate(new_platform_tasks):
            pools_chain[n][m] = new_platform_task

    new_pools_chain = list()
    for pool in pools_chain:
        new_pool = list()
        for task in pool:
            if task is not None:
                new_pool.append(task)
        new_pools_chain.append(new_pool)
    return new_pools_chain

def create_tasks_pools_chain(browser):
    platforms: list = [JoyreactorScrapper(browser), PikabuScrapper(browser)]
    platforms_tasks = [platform.create_platform_task() for platform in platforms]
    tasks_pools_chain = make_pools_chain(platforms_tasks)
    return tasks_pools_chain

async def get_posts_chunk():
    playwright, browser = await _init_browser()
    try:
        tasks_pools_chain = create_tasks_pools_chain(browser)
        for tasks_pool in tasks_pools_chain:
            platforms_posts_chunk = await asyncio.gather(*tasks_pool)  # [[Post, Post], [Post], [Post], ...]
            posts_chunk = list(chain.from_iterable(platforms_posts_chunk))  # [Post, Post, Post, Post]

            logger.info("%s received %s posts", asyncio.current_task().get_name(), len(posts_chunk))
            yield posts_chunk
        logging.info("Exit from tasks chain")
    finally:
        await _close_browser(playwright, browser)

async def take_posts():
    async for posts_chunk in get_posts_chunk():
        # тут можно asyncio.Queue

        posts_chunk = await PostsFilter(posts_chunk).filter_posts()  # вернёт массив где
        logger.debug("Posts has been filtered out. Posts in chunk: %s", len(posts_chunk))

        posts_chunk = await MediaDownloader(posts_chunk).download_posts_media()
        logger.debug("Posts media has been downloaded. Posts in chunk: %s", len(posts_chunk))

        posts_chunk = await PostsCategorizer(posts_chunk).set_category_by_ai()
        logger.debug("Posts media has been categorized. Posts in chunk: %s", len(posts_chunk))

        uploading_data = await DatabaseManager().add_posts(posts_chunk)
        logger.debug("Posts media has been upload in database: %s", uploading_data)

        logger.debug("The result of the work: %s", posts_chunk)

# celery
