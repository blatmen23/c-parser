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


class JoyreactorScrapper(Scrapper):
    def __init__(self, browser: Browser, urls: list[str] = None):
        default_urls = ["https://joyreactor.cc/",
                        "https://joyreactor.cc/new",
                        "https://joyreactor.cc/best"]
        super().__init__(browser, urls or default_urls)

    async def get_posts(self, url: str) -> list[Post]:
        page_content = await super().fetch_dynamic_page(url)
        return await self.parse_posts(page_content)

    @classmethod
    async def parse_posts(cls, page_content: str):
        await asyncio.sleep(1)
        soup = BeautifulSoup(page_content, 'html.parser')
        posts = list()

        stories = soup.find_all("div", class_=["content-card", "post-card"])
        for story in stories:
            try:
                identifier = cls._get_source(story).url.split("/")[-1]
                # category
                media = await cls._get_media_contents(story)
                # comments
                source = cls._get_source(story)
                title = cls._get_title(story)
                caption = cls._get_caption(story)
                create_at = datetime.datetime.now()
                posts_tags = cls._get_tags(story)
            except KeyError:
                logger.info("Parsing exception KeyError")
                continue
            except AttributeError:
                logger.info("Parsing exception AttributeError")
                continue
            # print("identifier", identifier)
            # print("media", media)
            # print("source", source)
            # print("title", title)
            # print("caption", caption)
            # print("create_at", create_at)
            # print("posts_tags", posts_tags)
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
        post_content = story.find("div", class_="post-content")
        media_content: list[MediaContent] = list()

        image = post_content.find("div", class_="image")
        if image is not None:
            media_img = image.find("img")
            media_url = media_img["src"]
            if not media_url:
                logger.debug("Not find image url for: %s", cls._get_source(story).url)
            file_type = cls.get_file_type(media_url.split(".")[-1])

            media_headers = await super().get_response_headers(media_url)
            file_size = int(media_headers["Content-Length"])

            media_content.append(MediaContent(
                media_type=MediaTypes.IMAGE,
                media_url=media_url,
                file_type=file_type,
                file_size=file_size,
                file_hash=None))

        video = post_content.find("video")
        if video is not None:
            video_source = video.find("source", type="video/mp4")
            if not video_source:
                return media_content
            media_url = video_source["src"]
            if not media_url:
                logger.debug("Not find video url for: %s", cls._get_source(story).url)

            file_type = cls.get_file_type(media_url.split(".")[-1])

            headers = {
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

            media_headers = await super().get_response_headers(media_url, headers=headers)
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
        post_footer = story.find("div", class_="post-footer")
        url = "https://joyreactor.cc" + post_footer.find("a", target="_blank")["href"]
        story_datetime = post_footer.find("div", class_="ml-2").text.strip()

        posting_at = datetime.datetime.strptime(story_datetime, "%d.%m.%y, %H:%M")

        source = Source(
            url=url,
            platform=Platforms.JOYREACTOR,
            posting_at=posting_at
        )
        return source

    @classmethod
    def _get_title(cls, story):
        post_content = story.find("div", class_="post-content")
        post_title = post_content.find("h3")
        return None if post_title is None else post_title.text.strip()

    @classmethod
    def _get_caption(cls, story):
        post_content = story.find("div", class_="post-content")
        caption_spans = post_content.find_all("span")
        if caption_spans:
            caption = ""
            for caption_span in caption_spans:
                caption += caption_span.text + "\n"
            return caption if caption != "" else None
        else:
            None

    @classmethod
    def _get_tags(cls, story):
        tags_container = story.find("div", class_="post-tags")
        tags = [tag.text for tag in tags_container.find_all("span", class_=["ant-tag", "tag-reactor"])]
        return tags
