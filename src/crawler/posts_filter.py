from src.schemas.schemas import Post

class PostsFilter:
    def __init__(self, posts: list[Post]):
        self.posts = posts

    def _clear_duplicates_posts(self):
        seen = set()
        f: bool = lambda post: post.identifier not in seen and not seen.add(post.identifier)
        self.posts = list(filter(f, self.posts))

    async def _clear_existing_posts(self):
        ...
        # self.posts =

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
        self._clear_no_valid_posts()
        return self.posts
