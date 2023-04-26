import asyncio

import asyncpg
import pytest

from typing import AsyncGenerator

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from app.database import get_async_session, metadata
from app.main import app

DATABASE_URL_TEST = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}_test'

engine_test = create_async_engine(DATABASE_URL_TEST)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


async def create_db_if_not_exists():
    conn = await asyncpg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                 host=POSTGRES_HOST, port=POSTGRES_PORT, database='postgres')
    db_name = f'{POSTGRES_DB}_test'
    exists = await conn.fetchval('SELECT EXISTS(SELECT datname FROM pg_database WHERE datname = $1)', db_name)
    if not exists:
        await conn.execute(f'CREATE DATABASE {db_name}')

        db_conn = await asyncpg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                        host=POSTGRES_HOST, port=POSTGRES_PORT, database=db_name)
        await db_conn.execute(f'CREATE EXTENSION postgis;')
        await db_conn.close()
    await conn.close()


async def drop_db():
    conn = await asyncpg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                 host=POSTGRES_HOST, port=POSTGRES_PORT, database='postgres')
    db_name = f'{POSTGRES_DB}_test'
    await conn.execute(
        f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
        f"FROM pg_stat_activity "
        f"WHERE datname = '{db_name}' AND pid <> pg_backend_pid()"
    )
    await conn.execute(f'DROP DATABASE IF EXISTS {db_name}')
    await conn.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    await create_db_if_not_exists()
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await drop_db()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac
