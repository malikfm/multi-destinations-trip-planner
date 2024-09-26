import heapq
import sqlite3
from copy import deepcopy
from math import asin, cos, radians, sin, sqrt
from typing import Dict, List, Tuple

from fastapi import HTTPException

from trip_repository import TripRepository


def haversine_formula(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6372.8  # Earth's radius in kilometers

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(delta_lon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))

    return R * c


def calculate_distances(start: Dict, itinerary: List[sqlite3.Row]) -> List[float]:
    distances = []
    current = deepcopy(start)

    for destination in itinerary:
        distance = haversine_formula(
            current["latitude"],
            current["longitude"],
            destination["latitude"],
            destination["longitude"],
        )
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
        self, hotel_id: int, tag: str, max_destinations: int = 5
    ) -> Tuple[List[sqlite3.Row], List[Tuple[int, float]], float]:

        hotel = self.trip_repository.get_hotel_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        destinations = self.trip_repository.get_tourism_spots_by_tag(tag)
        if not destinations:
            return [], [], 0

        all_eligible_places = {
            f"hotel_{hotel["id"]}": {
                "name": hotel["name"],
                "latitude": hotel["latitude"],
                "longitude": hotel["longitude"],
            }
        }
        for destination in destinations:
            all_eligible_places[f"{destination["id"]}"] = {
                "name": destination["name"],
                "latitude": destination["latitude"],
                "longitude": destination["longitude"],
            }

        # Priority queue (open list)
        open_list = []

        # Start from the hotel
        # (f_score, current_node, g_score, path, distance of each destination, stops)
        heapq.heappush(open_list, (0, f"hotel_{hotel["id"]}", 0, 0, 0))
        distances = []
        paths = []

        visited = set()  # Closed list to keep track of visited spots.

        iter_num = 0
        while open_list:
            # Get node with lowest f_score then clear the rest so no duplicate element.
            _, current_id, g_score, distance, stops = heapq.heappop(open_list)
            open_list.clear()

            # Get the current node (hotel or tourism spot)
            if iter_num > 0:
                current_node = all_eligible_places[current_id]
            else:
                current_node = all_eligible_places[f"hotel_{hotel["id"]}"]

            # if iter_num > 0:
            #     # Add current node to the path except hotel.
            paths.append(current_node["name"])
            distances.append(distance)

            # Stop if we have visited enough spots (max_destinations)
            if stops == max_destinations:
                # Distance from last destination to hotel.
                last_distance = haversine_formula(
                    current_node["latitude"],
                    current_node["longitude"],
                    hotel["latitude"],
                    hotel["longitude"]
                )

                # Add hotel again to the last.
                paths.append(paths[0])
                distances.append(last_distance)

                total_distance = g_score + last_distance

                return paths, distances, total_distance

            visited.add(current_id)

            # Explore neighbors (all other unvisited spots)
            for neighbor_id, neighbor in all_eligible_places.items():
                if neighbor_id in visited:
                    continue  # Skip visited nodes

                # Distance from the current node to the neighbor
                distance = haversine_formula(
                    current_node["latitude"],
                    current_node["longitude"],
                    neighbor["latitude"],
                    neighbor["longitude"],
                )

                # Actual cost (g): The actual distance travelled so far (to the neighbor)
                g = g_score + distance

                # Heuristic (h): Distance from the neighbor to the nearest unvisited spot
                # Here, the heuristic is simply the nearest unvisited spot
                nearest_unvisited_spots = [
                    n
                    for n_id, n in all_eligible_places.items()
                    if n_id not in visited and n_id != neighbor_id
                ]

                # Because max destinations = 5, no need to look up nearest unvisited spots from neighbor if current node
                #  is the 4th node.
                if nearest_unvisited_spots and stops < (max_destinations - 2):
                    h = min(
                        haversine_formula(
                            neighbor["latitude"],
                            neighbor["longitude"],
                            n["latitude"],
                            n["longitude"],
                        )
                        for n in nearest_unvisited_spots
                    )
                else:
                    h = 0  # All spots have been visited or current node = node before last node.

                # Total cost f = g + h
                f = g + h

                # Add neighbor to the open list with updated f_score, g_score, and path
                heapq.heappush(
                    open_list,
                    (f, neighbor_id, g, distance, stops + 1),
                )

            iter_num += 1

        return [], [], 0  # No valid path found
