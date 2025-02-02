from typing import List, Tuple

from app.models import City
from app.repositories import CityRepository
from app.schemas import (
    CityNameModel, CityNameSchema, CityModel, LatitudeLongtitudeSchema
)
from app.db.core import async_session_maker
from app.errors import NotUniqueCityExc, NoSuchCityExc
from app.config import config
from .abstracts import IService
from .external_fetcher import APIDataFetcher


class CityService(IService[City]):
    def __init__(
        self,
        city_repository: CityRepository = CityRepository(),
        data_fetcher: APIDataFetcher = APIDataFetcher()
    ):
        self._repository = city_repository
        self.data_fetcher = data_fetcher

    @property
    def repository(self) -> CityRepository:
        return self._repository

    async def create(self, model: CityNameModel) -> CityModel:
        async with async_session_maker() as db_session:
            if await self.repository.get_by_name(model.name, db_session):
                raise NotUniqueCityExc()
            latitude, longtitide = await self.data_fetcher.fetch(model.name)
            model_data = {
                **dict(CityNameSchema().dump(model)),
                'latitude': latitude,
                'longtitude': longtitide
            }
            city = await self.repository.create(model_data, db_session)
            return CityModel(
                city_id=city.city_id,
                name=city.name,
                latitude=city.latitude,
                longtitude=city.longtitude
            )

    async def get_page(self, page: int) -> Tuple[int, List[CityModel]]:
        async with async_session_maker() as db_session:
            total_count = await self.repository.get_count(db_session)
            offset = (page - 1) * config.PAGE_LIMIT
            cities = await self.repository.get_chunk(
                offset, config.PAGE_LIMIT, db_session
            )
            return total_count, [
                CityModel(
                    city_id=city.city_id,
                    name=city.name,
                    latitude=city.latitude,
                    longtitude=city.longtitude
                ) for city in cities
            ]

    async def delete(self, city_id: int) -> None:
        async with async_session_maker() as db_session:
            city = await self.repository.get_by_id(city_id, db_session)
            if not city:
                raise NoSuchCityExc()
            await self.repository.delete(city, db_session)

    async def get_closest_cities(
        self, dot_schema: LatitudeLongtitudeSchema
    ) -> List[CityModel]:
        async with async_session_maker() as db_session:
            cities = await self.repository.get_closest_cities(
                dot_schema.latitude, dot_schema.longtitude, db_session
            )
            return [
                CityModel(
                    city_id=city.city_id,
                    name=city.name,
                    latitude=city.latitude,
                    longtitude=city.longtitude
                ) for city in cities
            ]
