import asyncio
from abc import ABC, abstractmethod
from aiohttp_socks import ProxyConnector
import logging

from fake_useragent import UserAgent
from aiohttp import ClientSession, ClientTimeout
from playwright.async_api import Browser, BrowserContext, Page, TimeoutError

from src.schemas.schemas import Post
from src.schemas.enums import FileTypes, Platforms

logger = logging.getLogger(__name__)


class Scrapper(ABC):
    def __init__(self, browser: Browser, urls: list[str] = None):
        self.browser = browser
        self.urls = urls

    @abstractmethod
    async def get_posts(self, url) -> list[Post]:
        pass

    @classmethod
    @abstractmethod
    def parse_posts(cls, page_content: str):
        pass

    def create_platform_task(self):
        return [self.get_posts(url) for url in self.urls]

    @staticmethod
    def get_file_type(file_extension: str):
        for file_type in FileTypes:
            if file_type.value == file_extension:
                return file_type
        return FileTypes.OTHER

    @staticmethod
    def get_request_headers(platform: str = None):
        match platform:
            case Platforms.JOYREACTOR.value:
                return {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "cookie": "surfer_uuid=f31ab800-c4d8-45c9-840c-361dc87e0feb; _ga=GA1.1.1594363128.1740469405; la_page_depth=%7B%22last%22%3A%22https%3A%2F%2Fjoyreactor.cc%2Fpost%2F6036462%22%2C%22depth%22%3A41%7D; _ga_YJ8SHVXBVL=GS1.1.1740509271.3.1.1740509817.0.0.0",
                    "priority": "u=0, i",
                    "referer": "https://joyreactor.cc/",
                    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
                }
            case _:
                return {
                    "User-Agent": UserAgent().random,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Referer": "https://www.google.com/",
                    "X-Requested-With": "XMLHttpRequest"  # Для AJAX-запросов
                }

    @classmethod
    async def get_response_headers(cls, url, headers: dict = None):
        async with cls.create_aiohttp_session() as session:
            response = await session.head(url, headers=headers or cls.get_request_headers())
            return response.headers

    @staticmethod
    def get_aiohttp_proxy():
        pass

    @staticmethod
    def get_playwright_proxy():
        pass

    @staticmethod
    def create_aiohttp_session(use_proxy: bool = False) -> ClientSession:
        # потом этот юрл будем брать с методов каких-то
        url = "socks5://sEefSS:RvzNqj@168.80.1.60:8000"
        connector = ProxyConnector.from_url(url=url)

        if not use_proxy:
            return ClientSession(trust_env=True, timeout=ClientTimeout(total=5))
        return ClientSession(trust_env=True, timeout=ClientTimeout(total=5), connector=connector)

    async def fetch_static_page(self, url: str, headers: dict = None, proxy: str = None):
        async with self.create_aiohttp_session() as session:
            async with session.get(url, headers=headers, proxy=proxy) as response:
                return await response.text()

    async def fetch_dynamic_page(self, url: str, headers: dict = None, proxy: str = None):
        context = await self.browser.new_context()
        page = await context.new_page()

        try:
            # Устанавливаем таймаут 5 секунд (5000 миллисекунд)
            await page.goto(url, timeout=5000)
        except TimeoutError:
            # Если страница не загрузилась за 5 секунд, просто продолжаем выполнение
            logger.debug("Page did not loaded in 5 seconds: %s", url)

        content = await page.content()
        await page.close()
        await context.close()
        return content
