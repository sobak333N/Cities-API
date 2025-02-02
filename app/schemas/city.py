from marshmallow import Schema, fields, post_load, validate
from dataclasses import dataclass


@dataclass
class CityModel:
    city_id: int
    name: str
    latitude: float
    longtitude: float


@dataclass
class DotModel:
    latitude: float
    longtitude: float


class CitySchema(Schema):
    """Схема описывающая информацию о городе."""
    city_id = fields.Integer(
        metadata={"description": "Уникальный идентификатор города"}
    )
    name = fields.String(
        required=True, 
        metadata={"description": "Название города"}
    )
    latitude = fields.Float(
        metadata={"description": "Широта"}
    )
    longtitude = fields.Float(
        metadata={"description": "Долгота"}
    )

    @post_load
    def make_city(self, data, **kwargs):
        return CityModel(**data)


class CityQuerySchema(Schema):
    """Схема запроса для пагинации"""
    page = fields.Integer(required=True, metadata={"description": "Номер страницы", "example": 1})


class CityListResponseSchema(Schema):
    """Схема ответа, возвращает список городов и общее количество"""
    total_count = fields.Integer(metadata={"description": "Общее количество городов"})
    cities = fields.List(fields.Nested(CitySchema), metadata={"description": "Список городов"})


class LatitudeLongtitudeSchema(Schema):
    """Схема запроса для получения двух ближайших городов к заданной точке"""
    latitude = fields.Float(
        required=True, 
        validate=validate.Range(min=-90, max=90),
        metadata={"description": "Широта точки. От -90 до 90 градусов.", "example": 45.454545},
    )
    longtitude = fields.Float(
        required=True, 
        validate=validate.Range(min=-180, max=180),
        metadata={"description": "Долгота точки. От -180 до 180 градусов.", "example": 53.535353},
    )

    @post_load
    def make_dot(self, data, **kwargs):
        return DotModel(**data)
    
    class Meta:
        ordered = True