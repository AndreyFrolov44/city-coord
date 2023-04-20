from typing import List, Optional

from geopy import Location
from geopy.adapters import AioHTTPAdapter
from sqlalchemy import delete, select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.geocoders import Nominatim
from fastapi import HTTPException, status

from cities.models import cities
from cities.schemas import City, CityDistance


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


async def delete_city_handler(name: str, session: AsyncSession):
    query = delete(cities).where(cities.c.name == name).returning(cities.c.name)
    result = await session.execute(query)
    if not result.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City not found')
    await session.commit()


async def get_by_city_name(name: str, session: AsyncSession) -> City:
    query = select(cities).where(cities.c.name == name)
    result = await session.execute(query)
    city = result.first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City not found')
    return City(name=city.name, lat=city.lat, lon=city.lon)


async def get_nearest_cities_handler(lat: float, lon: float, session: AsyncSession) -> List[City]:
    query = (
        select(
            cities,
            func.ST_DistanceSphere(
                func.ST_MakePoint(cities.c.lon, cities.c.lat),
                func.ST_MakePoint(lon, lat)
            ).label('distance')
        )
        .order_by('distance')
        .limit(2)
    )
    result = await session.execute(query)
    return [CityDistance(name=city.name, lat=city.lat, lon=city.lon, distance=city.distance) for city in result.all()]
