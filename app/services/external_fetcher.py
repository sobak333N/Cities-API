from typing import Tuple

from aiohttp import ClientSession

from .abstracts import IDataFetcher
from app.config import config
from app.errors import NoSuchCityExc, ForeignServiceExc


class APIDataFetcher(IDataFetcher):
    def __init__(self, base_url: str = config.FETCH_URL):
        self.base_url = base_url

    async def fetch(self, city: str) -> Tuple[float, float]:
        url = f"{self.base_url}{city}"
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status != 200 and response.status != 404:
                    raise ForeignServiceExc()
                if response.status == 404:
                    raise NoSuchCityExc()
                try:
                    response_json = await response.json()
                    city_info = response_json[0]
                    return (float(city_info['lat']), float(city_info['lon']))
                except (IndexError, KeyError):
                    raise NoSuchCityExc()
