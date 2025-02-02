from aiohttp import web
from aiohttp_apispec import (
    docs, request_schema, response_schema, querystring_schema
)

from app.schemas import ( 
    CityNameSchema, CitySchema, CityQuerySchema, CityListResponseSchema,
    EmptySchema, LatitudeLongtitudeSchema,
)
from app.services import CityService
from app.errors import MissingParametrExc
from app.utils import handle_query


CITY_API_PREFIX = "/city"
city_service = CityService()


@docs(
    tags=["Cities"],
    summary="Create city in storage",
    description="Добавляет город по названию",
)
@request_schema(CityNameSchema)
@response_schema(CitySchema, 201)
async def post_city(request: web.Request):
    data = await request.json()
    schema = CityNameSchema().load(data)
    city = await city_service.create(schema)
    return web.json_response(
        CitySchema().dump(city),
        status=201
    )


@docs(
    tags=["Cities"],
    summary="Get List of cities",
    description="Получает список",
)
@querystring_schema(CityQuerySchema)
@response_schema(CityListResponseSchema, 200)
async def get_list_cities(request: web.Request):
    page = handle_query(request, "page")
    total_count, cities = await city_service.get_page(int(page))
    return web.json_response(
        {
            "cities": CitySchema(many=True).dump(cities),
            'total_count': total_count
        },
        status=200
    )    


@docs(
    tags=["Cities"],
    summary="Delete city by id",
    description="Удаляет город по уникальному идентификатору",
)
@response_schema(EmptySchema, 204)
async def delete_city(request: web.Request):
    city_id = request.match_info.get("city_id")
    if not city_id or not city_id.isdigit():
        raise MissingParametrExc(field_name="city_id")
    await city_service.delete(int(city_id))
    return web.json_response(status=204)   


@docs(
    tags=["Cities"],
    summary="Get closest cities to dot",
    description="Получает ближайшие к заданной точке города",
)
@querystring_schema(LatitudeLongtitudeSchema)
@response_schema(CityListResponseSchema, 200)
async def get_closest_cities(request: web.Request):
    handle_query(request, "latitude")
    handle_query(request, "longtitude")
    schema = LatitudeLongtitudeSchema().load(request.query)
    cities = await city_service.get_closest_cities(schema)
    return web.json_response(
        {
            "cities": CitySchema(many=True).dump(cities),
            "total_count": len(cities)
        },
        status=200
    )


def setup_cities_routes(app: web.Application):
    app.router.add_post(f'{CITY_API_PREFIX}/post', post_city)
    app.router.add_get(f'{CITY_API_PREFIX}/get/', get_list_cities)
    app.router.add_delete(f'{CITY_API_PREFIX}/delete/{{city_id}}', delete_city)
    app.router.add_get(f'{CITY_API_PREFIX}/closest_cities', get_closest_cities)
