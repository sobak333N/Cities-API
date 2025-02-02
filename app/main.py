from aiohttp import web
from app.routes import setup_routes
from app.middlewares import error_middleware


def init_app():
    app = web.Application(middlewares=[error_middleware])
    setup_routes(app)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8000)
