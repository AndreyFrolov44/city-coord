from typing import List, Optional

from geopy import Location
from geopy.adapters import AioHTTPAdapter
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.geocoders import Nominatim
from fastapi import HTTPException, status

from cities.models import cities
from cities.schemas import City


async def get_locations(city_name: str) -> Optional[List[Location]]:
    async with Nominatim(
            user_agent='cities',
            adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        return await geolocator.geocode(
            {'city': city_name},
            addressdetails=True,
            exactly_one=False,
            language='en',
            featuretype='city',
            namedetails=True
        )


async def create_city_handler(city_name: str, session: AsyncSession) -> List[City]:
    locations = await get_locations(city_name)

    if not locations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City with this name not found')

    cities_list = []
    values_list = []
    points = []

    for location in locations:
        city = City(
            name=location.address,
            lat=location.latitude,
            lon=location.longitude,
        )
        values = {**city.dict()}
        if location.point not in points:
            points.append(location.point)
            cities_list.append(city)
            values_list.append(values)

    query = insert(cities).values(values_list) \
        .on_conflict_do_nothing(index_elements=['lat', 'lon']) \
        .returning(cities.c.name, cities.c.lat, cities.c.lon)

    result = await session.execute(query)
    insert_cities = result.all()

    await session.commit()

    if not insert_cities:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The city already exists')

    return [City(
                name=city.name,
                lat=city.lat,
                lon=city.lon
            ) for city in insert_cities]
