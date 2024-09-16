from typing import List, Tuple
from math import sqrt

from fastapi import HTTPException

from trip_repository import TripRepository


def euclidian_distance(x1: float, x2: float, y1: float, y2: float) -> float:
    delta_x = x2 - x1
    delta_y = y2 - y1

    return sqrt((delta_x ** 2) + (delta_y ** 2))


def calculate_distances(start: Tuple[float, float], itinerary: List[Tuple[int, str, float, float]]) -> List[float]:
    distances = []
    current = start

    for dest in itinerary:
        dist = euclidian_distance(current[0], current[1], dest[2], dest[3])
        distances.append(dist)
        current = (dest[2], dest[3])

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
    ) -> Tuple[List[Tuple[int, str, float, float]], List[float]]:

        hotel = self.trip_repository.get_hotel_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        start = (hotel[2], hotel[3])
        destinations = self.trip_repository.get_tourism_spots_by_tag(tag)

        if not destinations:
            return [], []

        unvisited = destinations[:]
        current = start
        itinerary = []

        while unvisited and len(itinerary) < max_destinations:
            next_dest = min(unvisited, key=lambda x: euclidian_distance(current[0], current[1], x[2], x[3]))
            itinerary.append(next_dest)
            current = (next_dest[2], next_dest[3])
            unvisited.remove(next_dest)

        distances = calculate_distances(start, itinerary)

        return itinerary, distances
