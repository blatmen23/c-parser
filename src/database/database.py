import logging
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)

url = URL.create(drivername="mariadb+aiomysql",
                 username="root",
                 password="",
                 host="localhost",
                 port=3306,
                 database="c_parser")  # .render_as_string(hide_password=False)

async_engine = create_async_engine(
    url=url,
    echo=False)

async_session_factory = async_sessionmaker(async_engine)

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                logger.exception("Error accessing the database. @connection")
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper