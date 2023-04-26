from httpx import AsyncClient

from app.cities.handlers import create_city_handler
from tests.conftest import async_session_maker


async def test_create_cities(ac: AsyncClient):
    response = await ac.post('/api/cities/create', params={'city_name': 'berlin'})

    assert response.status_code == 200
    assert len(response.json()) != 0
    assert {
               "name": "Berlin, Germany",
               "lat": 52.5170365,
               "lon": 13.3888599
           } in response.json()


async def test_delete_city_success(ac: AsyncClient):
    response = await ac.delete(
        '/api/cities/delete',
        params={'city_name': 'Berlin, Capitol Planning Region, United States'}
    )

    assert response.status_code == 200


async def test_delete_city_error(ac: AsyncClient):
    response = await ac.delete(
        '/api/cities/delete',
        params={'city_name': 'Madrid'}
    )

    assert response.status_code == 404


async def test_get_city_success(ac: AsyncClient):
    response = await ac.get(
        '/api/cities', params={'city_name': 'Berlin, Germany'}
    )

    assert response.status_code == 200
    assert response.json() == {
                    "name": "Berlin, Germany",
                    "lat": 52.5170365,
                    "lon": 13.3888599
                }


async def test_get_city_error(ac: AsyncClient):
    response = await ac.get(
        '/api/cities', params={'city_name': 'Madrid'}
    )

    assert response.status_code == 404


async def create_city(city_name: str):
    async with async_session_maker() as session:
        await create_city_handler(city_name, session)


async def test_nearest_city(ac: AsyncClient):
    await create_city('Rome')
    await create_city('San Marino')

    response = await ac.get(
        '/api/cities/nearest', params={'lat': 42.732344, 'lon': 12.437154}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {
            "name": "Rome, Roma Capitale, Lazio, Italy",
            "lat": 41.8933203,
            "lon": 12.4829321,
            "distance": 93371.20803817
        } in response.json()
    assert {
            "name": "San Marino, Montelaguardia, Perugia, Umbria, 06125, Italy",
            "lat": 43.1419676,
            "lon": 12.3839963,
            "distance": 45753.22711968
        } in response.json()


