from crawler.scrappers_control import start_tasks_chain
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s.%(msecs)3d] %(module)21s:%(lineno)-3d %(taskName)-6s %(levelname)-7s - %(message)s")

asyncio.run(start_tasks_chain())