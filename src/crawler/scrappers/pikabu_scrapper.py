import logging
import datetime
import json

from aiohttp import ClientSession
from playwright.async_api import Browser
from bs4 import BeautifulSoup

from src.crawler.scrappers.scrapper import Scrapper
from src.schemas.schemas import Post, MediaContent, Source
from src.schemas.enums import Platforms, MediaTypes

logger = logging.getLogger(__name__)


class PikabuScrapper(Scrapper):
    urls: list = ["https://pikabu.ru/",
                  "https://pikabu.ru/tag/Вертикальное%20видео"]
    # ,
    #                   "https://pikabu.ru/tag/Видео",
    #                   "https://pikabu.ru/tag/Юмор",
    #                   "https://pikabu.ru/tag/США"]
    @classmethod
    async def get_posts(cls, url: str, session: ClientSession, browser: Browser) -> list[Post]:
        page_content = await super().fetch_dynamic_page(url, browser)
        return cls._parse_posts(page_content)

    @classmethod
    def _parse_posts(cls, page_content: str):
        soup = BeautifulSoup(page_content, 'html.parser')
        posts = list()

        stories = soup.find_all("article", class_=["story", "story_redesign"])
        for story in stories:
            try:
                identifier = story['data-story-id']
                # category
                media = cls._get_media_contents(story)
                # comments
                source = cls._get_source(story)
                title = story.find("a", class_="story__title-link").text
                caption = cls._get_caption(story)
                create_at = datetime.datetime.now()
                posts_tags = cls._get_tags(story)
            except KeyError as e:
                logger.info("Parsing exception", exc_info=e)
                continue
            except AttributeError as e:
                logger.info("Parsing exception", exc_info=e)

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
    def _get_media_contents(cls, story):
        content_wrapper = story.find("div", class_="story__content-wrapper")
        media_content = list()

        images = content_wrapper.find_all("img", class_="story-image__image")
        for image in images:
            media_url = image["data-large-image"]
            file_type = cls._get_file_type(media_url.split(".")[-1])
            media_content.append(MediaContent(
                media_type=MediaTypes.IMAGE,
                file_type=file_type,
                media_url=media_url,
                media_hash=None))

        videos = content_wrapper.find_all("div", class_="player")
        for video in videos:
            media_url = video["data-webm"]
            if not media_url:
                logger.debug("Not find media url for: %s", cls._get_source(story).url)
                continue
            file_type = cls._get_file_type(media_url.split(".")[-1])
            media_content.append(MediaContent(
                media_type=MediaTypes.VIDEO,
                file_type=file_type,
                media_url=media_url,
                media_hash=None))
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
