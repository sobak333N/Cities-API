from aiohttp import web
from app.routes import setup_routes
from app.middlewares import error_middleware
from app.metrics import setup_metrics


def init_app():
    app = web.Application(middlewares=[error_middleware])
    setup_metrics(app)
    app.middlewares.append(error_middleware)
    setup_routes(app)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8000)
