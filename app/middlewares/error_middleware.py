
from aiohttp import web
# import logging
from marshmallow import ValidationError


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
    except web.HTTPException as ex:
        return web.json_response({"error": ex.reason}, status=ex.status)
    # except Exception as e:
    #     logging.exception("Unexpected server error")
    #     return web.json_response({"error": "Internal Server Error", "details": str(e)}, status=500)
