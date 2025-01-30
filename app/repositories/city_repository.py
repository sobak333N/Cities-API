from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from .abstracts import IRepository
from app.models import City


class CityRepository(IRepository[City]):
    async def create(
        self, model_data: dict, session: AsyncSession
    ) -> City:
        city = City(**model_data)
        session.add(city)
        await session.commit()
        return city

    async def get_by_name(
        self, name: str, session: AsyncSession
    ) -> Optional[City]:
        stmt = (select(City).where(City.name == name))
        result = await session.execute(stmt)
        city = result.scalars().one_or_none()
        return city

    async def delete(
        self, model: City, session: AsyncSession
    ) -> None:
        await session.delete(model)
        await session.commit()

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[City]:
        stmt = (select(City).where(City.city_id == id))
        result = await session.execute(stmt)
        city = result.scalars().one_or_none()
        return city

    async def get_chunk(
        self, offset: int, limit: int, session: AsyncSession
    ) -> List[City]:
        stmt = (select(City).order_by(City.city_id).offset(offset).limit(limit))
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_count(self, session: AsyncSession) -> int:
        stmt = (select(func.count()).select_from(City))
        result = await session.execute(stmt)
        return result.scalar() or 0
