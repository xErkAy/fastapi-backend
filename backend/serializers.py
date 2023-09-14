from datetime import datetime
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_queryset_creator, pydantic_model_creator

from exceptions import ValidationException
from models import City, Street, Shop

CitySerializer = pydantic_model_creator(City)
CitySerializer_List = pydantic_queryset_creator(City)

StreetSerializer = pydantic_model_creator(Street)
StreetSerializer_List = pydantic_queryset_creator(Street)

ShopSerializer = pydantic_model_creator(Shop)
ShopSerializer_List = pydantic_queryset_creator(Shop)


class RequestShopSerializer(BaseModel):
    name: str
    city_id: int
    street_id: int
    building: str
    open_time: str
    close_time: str

    @staticmethod
    def validate_time(time_str: list[str, str]) -> [datetime, datetime]:
        try:
            return [datetime.strptime(time_str[0], '%H:%M'), datetime.strptime(time_str[0], '%H:%M')]
        except ValueError:
            raise ValidationException('Invalid time format')

    async def save(self, data: dict) -> Shop:
        open_time, close_time = self.validate_time([data.get('open_time'), data.get('close_time')])
        if await Shop.filter(name=data.get('name'), street_id=data.get('street_id')).exists():
            raise ValidationException('The shop already exists')
        return await Shop.create(
            name=data.get('name'),
            city_id=data.get('city_id'),
            street_id=data.get('street_id'),
            building=data.get('building'),
            open_time=open_time,
            close_time=close_time
        )
