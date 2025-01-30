from app.models import City
from app.repositories import CityRepository
from app.schemas import (
    CityNameModel, CityNameSchema, CityModel, CitySchema
)
from app.db.core import async_session_maker
from app.errors import NotUniqueCityExc 
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



