from typing import List

from pydantic import BaseModel


class TripRequest(BaseModel):
    hotel_id: int
    tag: str


class TripLocation(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float


class TripPlan(BaseModel):
    destinations: List[str]
    distances: List[float]
    total_distance: float
