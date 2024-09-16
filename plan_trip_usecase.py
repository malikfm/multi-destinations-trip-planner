import sqlite3
from copy import deepcopy
from typing import List, Tuple, Dict
from math import sqrt, radians, sin, cos, atan2, asin

from fastapi import HTTPException

from trip_repository import TripRepository


def euclidian_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6372.8  # Earth's radius in kilometers

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = sin(delta_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(delta_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


def calculate_distances(start: Dict, itinerary: List[sqlite3.Row]) -> List[float]:
    distances = []
    current = deepcopy(start)

    for destination in itinerary:
        distance = euclidian_distance(current["latitude"], current["longitude"], destination["latitude"], destination["longitude"])
        distances.append(distance)

        current["latitude"] = destination["latitude"]
        current["longitude"] = destination["longitude"]

    return distances


class PlanTripUseCase:
    def __init__(self, trip_repository: TripRepository):
        self.trip_repository = trip_repository

    def show_all_hotels(self):
        return self.trip_repository.get_hotels()

    def show_all_tags(self):
        return self.trip_repository.get_tags()

    def plan_trip(
        self,
        hotel_id: int,
        tag: str,
        max_destinations: int = 5
    ) -> Tuple[List[sqlite3.Row], List[float]]:

        hotel = self.trip_repository.get_hotel_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        start = {"latitude": hotel["latitude"], "longitude": hotel["longitude"]}
        destinations = self.trip_repository.get_tourism_spots_by_tag(tag)

        if not destinations:
            return [], []

        current = deepcopy(start)
        unvisited = destinations[:]
        itinerary = []

        while unvisited and len(itinerary) < max_destinations:
            next_dest = min(
                unvisited,
                key=lambda x: euclidian_distance(current["latitude"], current["latitude"], x["latitude"], x["longitude"])
            )
            itinerary.append(next_dest)
            current["latitude"] = next_dest["latitude"]
            current["longitude"] = next_dest["longitude"]
            unvisited.remove(next_dest)

        distances = calculate_distances(start, itinerary)

        return itinerary, distances
