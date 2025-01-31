from abc import ABC, abstractmethod
import asyncio

from fake_useragent import UserAgent
from aiohttp import ClientSession
from playwright.async_api import Browser

from src.schemas.enums import FileTypes


class Scrapper(ABC):
    urls: list

    @classmethod
    @abstractmethod
    async def get_posts(cls, url, session: ClientSession, browser: Browser):
        pass

    @classmethod
    @abstractmethod
    def _parse_posts(cls, page_content: str):
        pass

    @classmethod
    def create_platform_task(cls):
        session: ClientSession
        browser: Browser
        session, browser = yield

        for url in cls.urls:
            session, browser = yield asyncio.create_task(
                cls.get_posts(url, session, browser))
        return None

    @classmethod
    def _get_file_type(cls, file_extension: str):
        for file_type in FileTypes:
            if file_type.value == file_extension:
                return file_type
        return FileTypes.OTHER

    @staticmethod
    def get_headers():
        return {
            "User-Agent": UserAgent().random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com/",
            "X-Requested-With": "XMLHttpRequest"  # Для AJAX-запросов
        }

    @staticmethod
    def get_aiohttp_proxy():
        pass

    @staticmethod
    def get_playwright_proxy():
        pass

    @staticmethod
    async def fetch_page(url: str, session: ClientSession, headers: dict = None, proxy: str = None):
        async with session.get(url, headers=headers, proxy=proxy) as response:
            return await response.text()

    @staticmethod
    async def fetch_dynamic_page(url: str, browser: Browser):
        context = await browser.new_context()
        # proxy = {
        #     "server": "proxy_host:port",
        #     "username": "your_username",
        #     "password": "your_password",
        # }
        page = await context.new_page()
        await page.goto(url)
        content = await page.content()
        await context.close()
        return content
