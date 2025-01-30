# app/routes/cities.py
from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import ValidationError

from app.schemas import CityNameSchema

# class NearestCitiesResponseSchema(web.Schema):
#     city1 = fields.Nested(CitySchema)
#     city2 = fields.Nested(CitySchema)
CITY_API_PREFIX = "/city"


@docs(
    tags=["Cities"],
    summary="Get two nearest cities",
    description="Возвращает два ближайших к заданной точке города",
)
@request_schema(CityNameSchema)
async def post_city(request):
    data = await request.json()
    schema = CityNameSchema().load(data)
    return web.json_response({"lox": 1})









@docs(
    tags=["Cities"],
    summary="Get two nearest cities",
    description="Возвращает два ближайших к заданной точке города",
)
# @request_schema(Location)
# @response_schema(NearestCitiesResponseSchema, 200)
async def get_nearest_cities(request):
    data = await request.json()
    input_lat = data["latitude"]
    input_lon = data["longitude"]
    response = {"city1": dict({"cities[0]":0}), "city2": dict({"cities[1]":1})}
    return web.json_response(response)


def setup_cities_routes(app: web.Application):
    # app.router.add_post('/city/nearest_cities', get_nearest_cities)
    app.router.add_post(f'{CITY_API_PREFIX}/post', post_city)

