from typing import Optional

from pydantic import BaseModel


class City(BaseModel):
    name: str
    lat: float
    lon: float
