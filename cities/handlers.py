from geopy.adapters import AioHTTPAdapter
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.geocoders import Nominatim

from cities.models import cities
from cities.schemas import City


async def get_coord_city(city_name: str) -> dict:
    async with Nominatim(
            user_agent="cities",
            adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode(city_name)

    return {'lat': location.latitude, 'lon': location.longitude}


async def create_city_handler(city_name: str, session: AsyncSession) -> City:
    coord = await get_coord_city(city_name)

    city = City(
        name=city_name,
        lat=coord['lat'],
        lon=coord['lon'],
    )

    values = {**city.dict()}
    values.pop('id', None)

    query = insert(cities).values(**values)

    result = await session.execute(query)
    await session.commit()

    city.id = result.inserted_primary_key[0]

    return city

