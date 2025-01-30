from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from app.schemas import CityNameSchema, CitySchema
from app.services import CityService

# class NearestCitiesResponseSchema(web.Schema):
#     city1 = fields.Nested(CitySchema)
#     city2 = fields.Nested(CitySchema)
CITY_API_PREFIX = "/city"
city_service = CityService()


@docs(
    tags=["Cities"],
    summary="Create city in storage",
    description="Добавляет город по названию",
)
@request_schema(CityNameSchema)
@response_schema(CitySchema, 201)
async def post_city(request):
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
    description="Добавляет город по названию",
)
@request_schema(CityNameSchema)
@response_schema(CitySchema, 201)
async def post_city(request):
    data = await request.json()
    schema = CityNameSchema().load(data)
    city = await city_service.create(schema)
    return web.json_response(
        CitySchema().dump(city),
        status=201
    )
# @docs(
#     tags=["Cities"],
#     summary="Delete city from storage",
#     description="Добавляет город по названию",
# )
# @request_schema(CityNameSchema)
# @response_schema(CitySchema, 201)
# async def post_city(request):
#     data = await request.json()
#     schema = CityNameSchema().load(data)
#     city = await city_service.create(schema)
#     return web.json_response(
#         CitySchema().dump(city),
#         status=201
#     )



def setup_cities_routes(app: web.Application):
    # app.router.add_post('/city/nearest_cities', get_nearest_cities)
    app.router.add_post(f'{CITY_API_PREFIX}/post', post_city)

