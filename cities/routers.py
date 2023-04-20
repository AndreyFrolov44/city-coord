from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.handlers import create_city_handler, delete_city_handler, get_by_city_name
from cities.schemas import City
from database import get_async_session

router = APIRouter(prefix='/cities', tags=['cities'])


@router.post('/create', response_model=List[City])
async def create_city(city_name: str, session: AsyncSession = Depends(get_async_session)) -> List[City]:
    return await create_city_handler(city_name, session)


@router.delete('/delete')
async def delete_city(name: str, session: AsyncSession = Depends(get_async_session)):
    return await delete_city_handler(name, session)


@router.get('')
async def get_city(name: str, session: AsyncSession = Depends(get_async_session)):
    return await get_by_city_name(name, session)
