from typing import List, Optional, Generic, TypeVar
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_chunk(
        self, offset: int, limit: int, session: AsyncSession
    ) -> List[T]:
        pass

    @abstractmethod
    async def create(self, model_data: dict, session: AsyncSession) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, model: T, session: AsyncSession) -> None:
        pass
