import asyncio
from asyncio import Semaphore
from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from src.data_classes import *
from .scrapper import Scrapper

class NineGAG(Scrapper):
    urls = ["https://9gag.com/fresh"] * 5

    @classmethod
    def create_platform_task(cls):
        session: ClientSession = yield

        for url in cls.urls:
            session: ClientSession = yield asyncio.create_task(cls._get_posts(session, url))
        return None

    @classmethod
    async def _get_posts(cls, session: ClientSession, url: str):
        await asyncio.sleep(1)

        # page = await cls._get_page(session, url)
        #
        # posts = await cls._parse_posts(page)

        return ['bbk 1', 'bbk 2']

    @classmethod
    async def _get_page(cls, session: ClientSession, url):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/avif,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "user-agent": UserAgent().random
        }
        return await session.get(url=url, headers=headers)

    @classmethod
    async def _parse_posts(cls, page: ClientResponse):
        soup = BeautifulSoup(await page.text(), 'html.parser')

        stories = soup.find_all("article", class_="story_redesign")

        posts = list()
        for story in stories:
            print(story.text)
            identifier = story.find("")

            # categories =

            # media =

            # comments =

            # source =

            # caption =

            title = story.find("h2", class_="story__title").text


            # posts.append(Post(
            #     identifier=,
            #     # category=,
            #     # media=,
            #     # comments=,
            #     source=,
            #     # caption=,
            #     create_at=,
            #     # posts_tags=,
            # ))
            # story_data = story.findall("div", class_="")

            # story_content = story.findall("div", class_="story__content-wrapper")
        return posts
# а можно же ещё цепочки из одинаковых платформ суммировать до максимальной длины платформы, чтоб не простаивали