import asyncio
import logging
import random
from pprint import pprint

from src.schemas.schemas import Post
from src.schemas.enums import Categories
from src.crawler.scrappers.scrapper import Scrapper

logger = logging.getLogger(__name__)
class PostsCategorizer:
    def __init__(self, posts: list[Post]):
        self.posts: list[Post] = posts

    async def set_random_category(self):
        posts = list()
        for post in self.posts:
            await asyncio.sleep(0.01)
            post.category = random.choice(list(Categories)).value
            posts.append(post)
        return posts

    def _get_labels(self):
        return [category.value for category in Categories]

    def _get_text(self, post: Post):
        text = f"""
Теги к посту: {", ".join(post.posts_tags) if post.posts_tags is not None else 'Нет тегов к посту'}
Текст к посту: Не будет
Содержит фото/видео: {'Нет' if post.media is None else 'Да'}"""
        return text

    async def set_category_by_ai(self):
        posts = list()
        for post in self.posts:

            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/fewShotTextClassification"

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Api-key AQVNwCcFlip3suCM_3hk01Kp4LXLjoodJL-lQKJ4"
            }

            prompt = {
                "modelUri": "cls://b1g0lldj70es9lgi90ki/yandexgpt/latest",
                "taskDescription": "Определи категорию к которой можно отнести пост с таким тегами и таким текстом."
                                   " Помни о том что к каждому посту могут идти фото или видео материалы"
                                   "- учитывай это, ведь тебе не видно полноты картины.",
                "labels": self._get_labels(),
                "text": self._get_text(post)
            }

            await asyncio.sleep(1)
            async with Scrapper.create_aiohttp_session(use_proxy=False) as session:
                response = await session.post(url=url,
                                              headers=headers,
                                              json=prompt)
                ai_answer = await response.json()

                predictions: list[dict] = ai_answer["predictions"]
                prediction = max(predictions, key=lambda p: p['confidence'])

                post.category = prediction["label"]
                posts.append(post)
        return posts

    # async def categorize_posts(self):
    #     # await self._set_random_category()
    #     try:
    #         await self._set_category_by_ai()
    #     except Exception:
    #         logger.debug("Error in categorize posts by AI", exc_info=True)
    #     return self.posts

