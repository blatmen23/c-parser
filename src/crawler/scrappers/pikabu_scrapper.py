import asyncio
import logging
import datetime
import json

from playwright.async_api import Browser
from bs4 import BeautifulSoup

from src.crawler.scrappers.scrapper import Scrapper
from src.schemas.schemas import Post, MediaContent, Source
from src.schemas.enums import Platforms, MediaTypes

logger = logging.getLogger(__name__)


class PikabuScrapper(Scrapper):
    def __init__(self, browser: Browser, urls: list[str] = None):
        default_urls = ["https://pikabu.ru/",
                        "https://pikabu.ru/tag/Вертикальное%20видео"
                        "https://pikabu.ru/tag/Видео",
                        "https://pikabu.ru/tag/Юмор",
                        "https://pikabu.ru/tag/США"]
        super().__init__(browser, urls or default_urls)

    async def get_posts(self, url: str) -> list[Post]:
        page_content = await super().fetch_dynamic_page(url)
        return await self.parse_posts(page_content)

    @classmethod
    async def parse_posts(cls, page_content: str):
        soup = BeautifulSoup(page_content, 'html.parser')
        posts = list()

        stories = soup.find_all("article", class_=["story", "story_redesign"])
        for story in stories:
            try:
                identifier = story['data-story-id']
                # category
                media = await cls._get_media_contents(story)
                # comments
                source = cls._get_source(story)
                title = story.find("a", class_="story__title-link").text
                caption = cls._get_caption(story)
                create_at = datetime.datetime.now()
                posts_tags = cls._get_tags(story)
            except KeyError:
                logger.info("Parsing exception KeyError")
                continue
            except AttributeError:
                logger.info("Parsing exception AttributeError")
                continue

            posts.append(Post(
                identifier=identifier,
                category=None,
                media=media,
                comments=None,
                source=source,
                title=title,
                caption=caption,
                create_at=create_at,
                posts_tags=posts_tags
            ))
        return posts

    @classmethod
    async def _get_media_contents(cls, story):
        content_wrapper = story.find("div", class_="story__content-wrapper")
        media_content: list[MediaContent] = list()

        images = content_wrapper.find_all("img", class_="story-image__image")
        for image in images:
            media_url = image["data-large-image"]
            if not media_url:
                logger.debug("Not find image url for: %s", cls._get_source(story).url)
                continue
            file_type = cls.get_file_type(media_url.split(".")[-1])

            media_headers = await super().get_response_headers(media_url)
            file_size = int(media_headers["Content-Length"])

            media_content.append(MediaContent(
                media_type=MediaTypes.VIDEO,
                media_url=media_url,
                file_type=file_type,
                file_size=file_size,
                file_hash=None))

        videos = content_wrapper.find_all("div", class_="player")
        for video in videos:
            media_url = video["data-webm"]
            if not media_url:
                logger.debug("Not find video url for: %s", cls._get_source(story).url)
                continue
            file_type = cls.get_file_type(media_url.split(".")[-1])

            media_headers = await super().get_response_headers(media_url)
            file_size = int(media_headers["Content-Length"])

            media_content.append(MediaContent(
                media_type=MediaTypes.VIDEO,
                media_url=media_url,
                file_type=file_type,
                file_size=file_size,
                file_hash=None))

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
        content_wrapper = story.find("div", class_="story__content-wrapper")
        caption_contents = content_wrapper.find_all("div", class_=["story-block", "story-block_type_text"])
        caption = "".join([caption_content.text for caption_content in caption_contents])
        return caption

    @classmethod
    def _get_tags(cls, story):
        tags_container = story.find("div", class_="story__collapsed-tags-container")
        tags = [tag["data-tag"] for tag in tags_container.find_all("a", class_="tags__tag")]
        return tags
