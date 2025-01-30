from marshmallow import Schema, fields, post_load
from dataclasses import dataclass


@dataclass
class CityModel:
    city_id: int
    name: str
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