from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.handlers import create_city_handler
from cities.schemas import City
from database import get_async_session

router = APIRouter(prefix='/cities', tags=['cities'])


@router.post('/create', response_model=List[City])
async def create_city(city_name: str, session: AsyncSession = Depends(get_async_session)) -> List[City]:
    return await create_city_handler(city_name, session)
