from typing import Optional

from pydantic import BaseModel


class City(BaseModel):
    id: Optional[int]
    name: str
    lat: float
    lon: float
