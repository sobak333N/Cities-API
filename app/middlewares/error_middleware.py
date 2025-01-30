
from aiohttp import web
from marshmallow import ValidationError
from app.errors import CustomHttpExc


@web.middleware
async def error_middleware(request, handler):
    """Глобальный обработчик ошибок"""
    try:
        response = await handler(request)
        return response
    except ValidationError as err:
        return web.json_response(
            {"error": "Not valid data", "details": err.messages}, status=422
        )
    except CustomHttpExc as ex:
        return web.json_response(
            {"error": ex.details, "details": ex.details},
            status=ex.status
        )
