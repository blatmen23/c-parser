import asyncio
import time
from asyncio import Semaphore
from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from src.data_classes import *
from .scrapper import Scrapper
import json

class PikabuScrapper(Scrapper):
    urls = ["https://pikabu.ru/",
            "https://pikabu.ru/tag/Вертикальное%20видео",
            "https://pikabu.ru/tag/Видео",
            "https://pikabu.ru/tag/Юмор"]

    @classmethod
    def create_platform_task(cls):
        session: ClientSession = yield

        for url in cls.urls:
            session: ClientSession = yield asyncio.create_task(cls._get_posts(session, url))
        return None

    @classmethod
    async def _get_posts(cls, session: ClientSession, url: str):
        await asyncio.sleep(1)

        page = await cls._get_page(session, url)

        posts = await cls._parse_posts(page)

        return posts

    @classmethod
    async def _get_page(cls, session: ClientSession, url):
        headers = {
            "accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": UserAgent().random
        }
        return await session.get(url=url, headers=headers)

    @classmethod
    def _get_file_type(cls, file_extension: str) -> FileTypes:
        for file_type in FileTypes:
            if file_type.value == file_extension:
                return file_type
        return FileTypes.OTHER

    @classmethod
    def _get_media_contents(cls, story):
        content_wrapper = story.find("div", class_="story__content-wrapper")
        media_content = list()

        try:
            images = content_wrapper.find_all("img", class_="story-image__image")
            for image in images:
                media_url = image["data-large-image"]
                file_type = cls._get_file_type(media_url.split(".")[-1])
                media_content.append(MediaContent(
                        media_type=MediaTypes.IMAGE,
                        file_type=file_type,
                        media_url=media_url,
                        media_hash=None))
        except:
            pass

        try:
            videos = content_wrapper.find_all("div", class_="player")
            for video in videos:
                media_url = video["data-webm"]
                file_type = cls._get_file_type(media_url.split(".")[-1])
                media_content.append(MediaContent(
                        media_type=MediaTypes.VIDEO,
                        file_type=file_type,
                        media_url=media_url,
                        media_hash=None))
        except:
            pass

        return media_content

    @classmethod
    def _get_source(cls, story):
        url = story.find("a", class_="story__title-link")["href"]
        story_data = story.find("script", type="application/ld+json").text
        story_dict = json.loads(story_data)
        posting_at = datetime.datetime.fromisoformat(story_dict["datePublished"]).timestamp()

        source = Source(
            url=url,
            platform=Platforms.PIKABU,
            posting_at=posting_at
        )
        return source

    @classmethod
    def _get_caption(cls, story):
        try:
            content_wrapper = story.find("div", class_="story__content-wrapper")
            caption_contents = content_wrapper.find_all("div", class_=["story-block", "story-block_type_text"])
            caption = "".join([caption_content.text for caption_content in caption_contents])
            return caption
        except:
            return "NoNe"

    @classmethod
    def _get_tags(cls, story):
        try:
            tags_container = story.find("div", class_="story__collapsed-tags-container")
            tags = [tag["data-tag"] for tag in tags_container.find_all("a", class_="tags__tag")]
            return tags
        except:
            return "NoNe"

    @classmethod
    async def _parse_posts(cls, page: ClientResponse):
        soup = BeautifulSoup(await page.text(), 'html.parser')

        stories = soup.find_all("article", class_=["story", "story_redesign"])

        posts = list()
        for story in stories:
            posts.append(Post(
                identifier=story['data-story-id'],
                category=Categories.NOT_SET,
                media=cls._get_media_contents(story),
                comments=None,
                source=cls._get_source(story),
                title=story.find("a", class_="story__title-link").text,
                caption=cls._get_caption(story),
                create_at=int(time.time()),
                posts_tags=cls._get_tags(story)
            ))
        return posts

# а можно же ещё цепочки из одинаковых платформ суммировать до максимальной длины платформы, чтоб не простаивали