from typing import Tuple, Generic, TypeVar
from abc import ABC, abstractmethod

from app.repositories.abstracts import IRepository


T = TypeVar('T')


class IDataFetcher(ABC):
    @abstractmethod
    async def fetch(self, city: str) -> Tuple[float, float]:
        pass


class IService(ABC, Generic[T]):
    @property
    @abstractmethod
    def repository(self) -> IRepository[T]:
        pass