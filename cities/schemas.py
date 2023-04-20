from pydantic import BaseModel


class City(BaseModel):
    name: str
    lat: float
    lon: float


class CityDistance(City):
    distance: float
