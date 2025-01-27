import asyncio

from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
# К КЛАССУ CONFIG НАДО ПРИМЕНИТЬ ПАТТЕРН СИНГЛТОНА!!!
url = URL.create(drivername="mariadb+aiomysql",
                 username="root",
                 password="",
                 host="localhost",
                 port=3306,
                 database="c_parser").render_as_string(hide_password=False)

async_engine = create_async_engine(
    url=url,
    echo=True
)

async_session_factory = async_sessionmaker(async_engine)
# from src.database.models import Base
# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     print('done')
# asyncio.run(create_tables())