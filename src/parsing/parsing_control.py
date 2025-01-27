import asyncio
from aiohttp import ClientSession, ClientTimeout

from .scrappers.pikabu import *
from .scrappers.nine_gag import *

platforms = [PikabuScrapper, NineGAG]


def _create_tasks_pool():
    platforms_gen = [platform.create_platform_task()
                     for platform in platforms]

    for platform_gen in platforms_gen:  # initializing generators
        platform_gen.send(None)

    session: ClientSession = yield

    while True:
        tasks_pool = list()
        for platform_gen in platforms_gen:
            try:
                tasks_pool.append(platform_gen.send(session))
            except StopIteration as e:
                tasks_pool.append(e.value)
        # print("task_pool:")
        # for task in tasks_pool:
        #     print("\t", task)
        only_tasks_pool = [task for task in tasks_pool if task is not None]
        session: ClientSession = yield only_tasks_pool

async def start_tasks_chain():
    tasks_pool_gen = _create_tasks_pool()
    tasks_pool_gen.send(None)

    counter = 0
    while True:
        async with ClientSession(trust_env=True, timeout=ClientTimeout(total=5)) as session:  # connector=100
            tasks_pool = tasks_pool_gen.send(session)

            if not tasks_pool:
                print("exit from tasks chain")
                break

            counter += 1
            result = await asyncio.gather(*tasks_pool)
            print(f"{counter}) {session}")
            for res in result:
                for post in res:
                    print(post, "\n")

# celery