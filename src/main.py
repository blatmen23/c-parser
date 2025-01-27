from parsing.parsing_control import start_tasks_chain
import asyncio

asyncio.run(start_tasks_chain())

# from aiohttp import ClientSession, ClientTimeout
# import asyncio
#
# headers = {
#     "accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br"
# }
#
# async def client():
#     async with ClientSession(trust_env=True, timeout=ClientTimeout(total=5)) as session:  # connector=100
#         page = await session.get("https://pikabu.ru/tag/Вертикальное%20видео", headers=headers)
#         # print("async", page.headers)
#
#         with open("page_async.html", "w") as f:
#             f.write(await page.text())
#
# asyncio.run(client())
#
# import requests
#
# answer = requests.get("https://pikabu.ru/tag/%D0%AE%D0%BC%D0%BE%D1%80", headers=headers)
# # print("sync", answer.headers)
#
# with open("page_sync.html", "w") as f:
#     f.write(answer.text)
