import heapq
from typing import List, Dict

from models.place import Place


def heuristic_estimator(current_place: Place, possible_destinations: List[Place]) -> float:
    """
    Estimate the distance from the starting city (origin) to the closest city in the cities list (destinations).

    Args:
        current_place: The starting city.
        possible_destinations: List of cities to calculate the distance to.

    Returns:
        A positive real number represents the estimated distance.
    """
    return min(current_place.distance(destination) for destination in possible_destinations)


def construct_path(came_from: Dict[str, str], current: str) -> List[str]:
    """
    Construct trip path.

    Args:
        came_from: hehe
        current: hehe

    Returns:
        hehe
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)

    print(f"path - {path}")

    return path[::-1]


class Planner:
    def __init__(self, places: List[Place]):
        self.places = {place.name: place for place in places}

    def a_star(self, start: str, goals: List[str]) -> List[str]:
        start_place = self.places[start]
        goal_places = [self.places[goal] for goal in goals]
        visited_places = set()  # Keep track of visited cities.

        open_set = [(0, start)]
        came_from = {}  # Key value pairs represent destination (key) and origin (value).
        g_score = {start: 0}  # Represents the cost of the path from the start node to the current node.

        # An estimated total cost of the path through the current node to the goal.
        f_score = {start: heuristic_estimator(start_place, goal_places)}

        while open_set:
            # Implement priority queue to automatically sort elements based on their priority.
            current = heapq.heappop(open_set)[1]

            if current in goals:
                return construct_path(came_from, current)

            visited_places.add(current)  # Mark current city as visited.

            for neighbor in self.places:
                if neighbor == current or neighbor in visited_places:  # Skip if already visited.
                    continue

                # This is the distance from the start to the current node
                #   plus the distance from the current node to the neighbor.
                #
                # It represents the total distance of the path we're currently exploring to reach this neighbor.
                tentative_g_score = g_score[current] + self.places[current].distance(self.places[neighbor])

                # 1. Checks if we haven't visited this neighbor before.
                # 2. Checks if we found a better (shorter) path to this neighbor than we knew before.
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic_estimator(self.places[neighbor], goal_places)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def generate_plan(self, start: str, destinations: List[str]) -> List[str]:
        itinerary = [start]
        current = start
        remaining_destinations = set(destinations)

        # TODO: add condition if recommended destinations = 5, stop the iteration.
        while remaining_destinations:
            next_leg = self.a_star(current, list(remaining_destinations))
            if not next_leg:
                break

            itinerary.extend(next_leg[1:])
            current = next_leg[-1]
            remaining_destinations.remove(current)

        return itinerary
