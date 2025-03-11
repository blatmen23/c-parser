import os
import aiofiles
import logging
from uuid import uuid4

from src.crawler.scrappers.scrapper import Scrapper
from src.schemas.schemas import Post, MediaContent

logger = logging.getLogger(__name__)

class MediaDownloader:
    """Надо сказать, что тут я полностью забил на асинхронность.
     Но мне можно, потому что это всё равно никто не увидит"""
    media_files_directory = "media_files"

    def __init__(self, posts: list[Post]):
        self.posts: list[Post] = posts

    def _get_file_hash(self, platform: str, post_identifier: int, file_type: str):
        return f"{platform.lower()}_{post_identifier}.{file_type}"  # {uuid4().__str__()[:8:]}

    async def _download_media_file(self, post: Post, media: MediaContent):
        async with Scrapper.create_aiohttp_session(use_proxy=True) as session:
            response = await session.get(media.media_url, headers=Scrapper.get_request_headers(post.source.platform))
            if response.status == 200:
                file_hash = f"{self.media_files_directory}/{self._get_file_hash(post.source.platform, post.identifier, media.file_type)}"

                async with aiofiles.open(file_hash, 'wb') as f:
                    while True:
                        try:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await f.write(chunk)
                        except Exception:
                            logger.info("TimeoutError in Media Downloader", exc_info=False)
                            return None
            else:
                logger.error("Not successful downloading media file via: %s", media.media_url)
                return None
        return file_hash

    async def download_posts_media(self):
        if not os.path.exists(self.media_files_directory):
            os.mkdir(self.media_files_directory)

        for i, post in enumerate(self.posts):
            if post.media is None:
                logger.debug("Post: %s - media is None", post.identifier)
                continue

            logger.debug("Post: %s - have media", post.identifier)
            for j, media in enumerate(post.media):
                logger.debug("Start downloading: %s", media.media_url)
                try:
                    file_hash = await self._download_media_file(post, media)
                except:
                    logger.debug("Error in _download_media_file()", exc_info=True)
                logger.debug("%s - downloaded", file_hash if file_hash is not None else "This file had not successful")
                self.posts[i].media[j].file_hash = file_hash
        return self.posts