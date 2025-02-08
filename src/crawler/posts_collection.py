from .posts_filter import PostsFilter
from .posts_media_downloader import MediaDownloader
from src.schemas.schemas import Post

class PostsCollection:
    def __init__(self, posts: list[Post]):
        self.posts = posts

    async def filter_posts(self):
        posts_filter = PostsFilter(self.posts)
        self.posts = await posts_filter.filter_posts()

    async def download_media(self):
        media_downloader = MediaDownloader(self.posts)
        self.posts = await media_downloader.download_media()

    async def save_in_db(self):
        pass