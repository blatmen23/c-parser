import logging

from src.schemas.schemas import Post
from src.database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class PostsFilter:
    def __init__(self, posts: list[Post]):
        self.posts = posts

    def _clear_duplicates_posts(self):
        seen = set()
        f: bool = lambda post: post.identifier not in seen and not seen.add(post.identifier)
        self.posts = list(filter(f, self.posts))

    async def _clear_existing_posts(self):
        not_exist_posts = list()
        for post in self.posts:
            post_exist = await DatabaseManager().post_exist(post.identifier)
            if not post_exist:
                not_exist_posts.append(post)
            else:
                logger.debug("%s post already exist in database - %s", post.identifier, post.source.url)
        self.posts = not_exist_posts

    def _clear_big_media_posts(self):
        valid_posts = list()
        for post in self.posts:
            if post.media is None:
                valid_posts.append(post)
                continue

            if all(media.file_size < (1024 * 1024 * 10) for media in post.media):
                valid_posts.append(post)
            else:
                post.media = None  # media -> None
                valid_posts.append(post)
        self.posts = valid_posts

    def _clear_no_valid_posts(self):
        ...
        # self.posts =

    async def filter_posts(self) -> list[Post]:
        """
        Фильтрует посты: удаляет дубликаты, существующие и невалидные посты.
        Возвращает отфильтрованный список постов.
        """
        self._clear_duplicates_posts()
        await self._clear_existing_posts()
        self._clear_big_media_posts()
        # self._clear_no_valid_posts()
        return self.posts
