import logging

from .posts_filter import PostsFilter
from .posts_media_downloader import MediaDownloader
from src.schemas.schemas import Post

logger = logging.getLogger(__name__)

class PostsCollection:
    def __init__(self, posts: list[Post]):
        self.posts = posts
        logger.debug("Posts in chunk: %s, a collection of posts has been created", len(self.posts))

    def filter_posts(self):
        posts_filter = PostsFilter(self.posts)
        self.posts = posts_filter.filter_posts()
        logger.debug("Posts in chunk: %s, the chunk of posts has been filtered out", len(self.posts))

    async def download_media(self):
        media_downloader = MediaDownloader(self.posts)
        self.posts = await media_downloader.download_posts_media()
        logger.debug("Posts in chunk: %s, the chunk of posts media has been downloaded", len(self.posts))

    async def save_in_db(self):
        pass