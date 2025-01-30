# app/routes/__init__.py
from aiohttp import web
from app.routes.city_route import setup_cities_routes
from aiohttp_apispec import setup_aiohttp_apispec


def setup_routes(app: web.Application):
    setup_cities_routes(app)

    setup_aiohttp_apispec(
        app=app,
        title="My API",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )
