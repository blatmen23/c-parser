from crawler.crawler_control import take_posts
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s.%(msecs)-3d] %(module)22s:%(lineno)-3d %(taskName)-8s %(levelname)-7s - %(message)s")

# from src.schemas.enums import Categories
# print([cat.value for cat in list(Categories)])

asyncio.run(take_posts())