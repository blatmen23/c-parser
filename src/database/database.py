from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

url = URL.create(drivername="mariadb+aiomysql",
                 username="root",
                 password="",
                 host="localhost",
                 port=3306,
                 database="c_parser").render_as_string(hide_password=False)

async_engine = create_async_engine(
    url=url,
    echo=True)

async_session_factory = async_sessionmaker(async_engine)
