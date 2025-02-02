from typing import Any

from aiohttp import web

from app.errors import MissingParametrExc


def handle_query(request: web.Request, key: str) -> Any:
    value = request.query.get(key)
    if not value:
        raise MissingParametrExc(field_name=key)
    return value