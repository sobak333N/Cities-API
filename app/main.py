from aiohttp import web
from app.routes import setup_routes
from app.middlewares import error_middleware

# Определение схемы ответа

# Настройка aiohttp-apispec
# setup_aiohttp_apispec(
#     app=app,
#     title="My API",
#     version="v1",
#     url="/api/docs/swagger.json",  # URL для спецификации OpenAPI
#     swagger_path="/api/docs",  # URL для Swagger UI
# )
def init_app():
    app = web.Application(middlewares=[error_middleware])
    setup_routes(app)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8000)
