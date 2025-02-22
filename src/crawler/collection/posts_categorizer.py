import asyncio
import logging
import random

from src.schemas.schemas import Post
from src.schemas.enums import Categories

logger = logging.getLogger(__name__)
class PostsCategorizer:
    def __init__(self, posts: list[Post]):
        self.posts: list[Post] = posts

    async def _set_random_category(self):
        posts = list()
        for i, post in enumerate(self.posts):
            await asyncio.sleep(0.01)
            post.category = random.choice(list(Categories)).value
            posts.append(post)
        self.posts = posts

    async def categorize_posts(self):
        await self._set_random_category()
        return self.posts

