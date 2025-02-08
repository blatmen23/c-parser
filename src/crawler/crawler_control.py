import logging
import asyncio
from itertools import chain
from aiohttp import ClientSession, ClientTimeout
from playwright.async_api import async_playwright
from playwright.async_api import Browser

from .scrappers import PikabuScrapper, NineGagScrapper
from .posts_collection import PostsCollection

logger = logging.getLogger(__name__)

platforms: list = [PikabuScrapper, PikabuScrapper]


async def _init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    logger.info("Playwright had been start")
    logger.info("Browser had been created")
    return playwright, browser


async def _close_browser(playwright, browser):
    await browser.close()
    await playwright.stop()
    logger.info("Browser had been closed")
    logger.info("Playwright had been stop")


def _create_tasks_pool():
    platforms_gen = [platform.create_platform_task()
                     for platform in platforms]
    for platform_gen in platforms_gen:
        platform_gen.send(None)
    logger.debug("Platforms generators initialized")

    session: ClientSession
    browser: Browser
    session, browser = yield

    while True:
        tasks_pool = list()
        for platform_gen in platforms_gen:
            try:
                tasks_pool.append(platform_gen.send((session, browser)))
            except StopIteration:
                logger.debug("StopIteration: %s", platform_gen)
        session, browser = yield tasks_pool

def _create_session() -> ClientSession:
    return ClientSession(trust_env=True, timeout=ClientTimeout(total=5))

async def _get_posts_chunk():
    playwright, browser = await _init_browser()
    try:
        tasks_pool_gen = _create_tasks_pool()
        tasks_pool_gen.send(None)
        logger.debug("Tasks chain generator initialized")

        while True:
            async with _create_session() as session:  # connector=100
                tasks_pool = tasks_pool_gen.send((session, browser))

                if not tasks_pool:
                    logging.info("Exit from tasks chain")
                    break

                platforms_posts_chunk = await asyncio.gather(*tasks_pool)  # [[Post, Post], [Post], [Post], ...]
                posts_chunk = list(chain.from_iterable(platforms_posts_chunk))  # [Post, Post, Post, Post]
                logger.info("%s received %s posts", asyncio.current_task().get_name(), len(posts_chunk))
                yield posts_chunk
    finally:
        await _close_browser(playwright, browser)


async def take_posts():
    async for posts_chunk in _get_posts_chunk():
        print(posts_chunk)
        # posts_collection_chunk = PostsCollection(posts_chunk)
        # await posts_collection_chunk.filter_posts()
        # await posts_collection_chunk.download_media()
# celery
