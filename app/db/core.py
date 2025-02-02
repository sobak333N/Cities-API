from sqlalchemy.ext.asyncio import (
    AsyncEngine, create_async_engine, async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

from app.config import config


class Base(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(
    config.DATABASE_URL,
    echo=True,
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
