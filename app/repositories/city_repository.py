from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from .abstracts import IRepository
from app.models import City
from app.config import config


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

    async def get_closest_cities(
        self, latitude: float, longtitude: float, session: AsyncSession,
    ) -> List[City]:
        distance_expr = 2 * 6371 * func.asin(
            func.sqrt(
                func.pow(func.sin(func.radians((City.latitude - latitude) / 2)), 2) +
                func.cos(func.radians(latitude)) *
                func.cos(func.radians(City.latitude)) *
                func.pow(func.sin(func.radians((City.longtitude - longtitude) / 2)), 2)
            )
        )
        stmt = (
            select(
                City,
                distance_expr
            )
            .order_by(distance_expr)
            .limit(config.CITIES_LIMIT)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())