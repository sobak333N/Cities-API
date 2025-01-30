from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
        self, id: int, session: AsyncSession
    ) -> None:
        pass
    
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[City]:
        pass
    
    async def get_chunk(
        self, offset: int, limit: int, session: AsyncSession
    ) -> List[City]:
        pass