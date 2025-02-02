from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import config


class Base(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(
    config.DATABASE_URL,
    echo=True,
)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
