from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    docs,
    request_schema,
    response_schema,
)
from marshmallow import Schema, fields


# Определение схемы ответа
class HelloSchema(Schema):
    message = fields.Str()

# Обработчик маршрута с документацией
@docs(
    tags=["Hello"],
    summary="Say hello",
    description="Возвращает приветственное сообщение",
    responses={200: {"description": "Успешный ответ", "schema": HelloSchema}},
)
async def hello(request):
    return web.json_response({"message": "Hello, aiohttp with apispec!"})

app = web.Application()
app.router.add_get('/hello', hello)

# Настройка aiohttp-apispec
setup_aiohttp_apispec(
    app=app,
    title="My API",
    version="v1",
    url="/api/docs/swagger.json",  # URL для спецификации OpenAPI
    swagger_path="/api/docs",  # URL для Swagger UI
)

if __name__ == '__main__':
    print("STARTER")
    web.run_app(app, host='0.0.0.0', port=8000)
