from datetime import datetime

from fastapi import FastAPI, Body
from pydantic_core import ValidationError
from tortoise import Tortoise

from utils import filter_city_street
from exceptions import ExceptionWithMessage, ValidationException
from models import City, Street, Shop
from serializers import (
    CitySerializer,
    CitySerializer_List,
    StreetSerializer,
    StreetSerializer_List,
    ShopSerializer,
    ShopSerializer_List,
    RequestShopSerializer
)
from os import environ as env

app = FastAPI()


@app.get('/api/city/', response_model=CitySerializer_List)
async def get_all_cities():
    return await City.all()


@app.get('/api/{city_id}/street/', response_model=StreetSerializer_List)
async def get_streets_by_city(city_id: int):
    return await Street.filter(city__id=city_id)


@app.get('/api/shop/')
async def get_shops(city: int | None = None, street: str | None = None, open: str | None = None):

    queryset = await Shop.all()

    print(type(queryset))

    if open is not None:
        now = datetime.now().time()
        if open in ['1', 'true', 'True']:
            queryset = await queryset.filter(open_time__lte=now, close_time__gte=now)
        else:
            queryset = await queryset.filter(open_time__gte=now, close_time__lte=now)

    return await filter_city_street(queryset, city=city, street=street)


@app.post('/api/shop/')
async def create_shop(payload: dict = Body(...)):
    try:
        data = RequestShopSerializer(**payload)
        return await data.save(data=payload)
    except ValidationError:
        return ExceptionWithMessage('Invalid data provided')
    except ValidationException as e:
        return ExceptionWithMessage(str(e))


@app.on_event("startup")
async def start_up():
    await Tortoise.init(
        db_url=f'asyncpg://{env.get("DB_USER")}:{env.get("DB_PASSWORD")}'
               f'@{env.get("DB_HOST")}:{env.get("DB_PORT")}/{env.get("DB_NAME")}',
        modules={
            'models': ['models']
        }
    )
    await Tortoise.generate_schemas(safe=True)


@app.on_event("shutdown")
async def shut_down():
    return await Tortoise.close_connections()
