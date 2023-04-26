from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cities.handlers import create_city_handler, delete_city_handler, get_by_city_name, get_nearest_cities_handler
from app.cities.schemas import City
from app.database import get_async_session

router = APIRouter(prefix='/cities', tags=['cities'])


@router.post('/create', response_model=List[City])
async def create_city(city_name: str, session: AsyncSession = Depends(get_async_session)) -> List[City]:
    return await create_city_handler(city_name, session)


@router.delete('/delete')
async def delete_city(city_name: str, session: AsyncSession = Depends(get_async_session)):
    return await delete_city_handler(city_name, session)


@router.get('')
async def get_city(city_name: str, session: AsyncSession = Depends(get_async_session)):
    return await get_by_city_name(city_name, session)


@router.get('/nearest')
async def get_nearest_cities(lat: float, lon: float, session: AsyncSession = Depends(get_async_session)):
    return await get_nearest_cities_handler(lat, lon, session)
