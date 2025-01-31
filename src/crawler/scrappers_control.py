import logging
import asyncio
from aiohttp import ClientSession, ClientTimeout
from playwright.async_api import async_playwright
from playwright.async_api import Browser

from .scrappers import PikabuScrapper, NineGagScrapper

logger = logging.getLogger(__name__)

platforms: list = [PikabuScrapper]


async def _init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    logger.info("Playwright had been start")
    logger.info("Browser had been init")
    return playwright, browser


async def _close_browser(playwright, browser):
    await browser.close()
    await playwright.stop()
    logger.info("Browser had been closed")
    logger.info("Playwright had been stop")


def create_tasks_pool():
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


async def start_tasks_chain():
    playwright, browser = await _init_browser()
    try:
        tasks_pool_gen = create_tasks_pool()
        tasks_pool_gen.send(None)
        logger.debug("Tasks chain generator initialized")

        while True:
            async with ClientSession(trust_env=True, timeout=ClientTimeout(total=5)) as session:  # connector=100
                tasks_pool = tasks_pool_gen.send((session, browser))

                if not tasks_pool:
                    logging.info("Exit from tasks chain")
                    break

                result = await asyncio.gather(*tasks_pool)
                logger.info("Posts taken %s", asyncio.current_task().get_name())
                # for posts in result:
                #     for post in posts:
                #         print(post, "\n")
    finally:
        await _close_browser(playwright, browser)

# celery
