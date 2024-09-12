from math import sqrt
from typing import Self


class Place:
    def __init__(self, name: str, lon: float, lat: float):
        self.name = name
        self.lon = lon
        self.lat = lat

    def distance(self, destination: Self) -> float:
        """
        Calculate euclidian distance to a given destination.

        :param destination: Destination place.
        :return: Euclidian distance in double precision.
        """
        delta_lon = destination.lon - self.lon  # delta x
        delta_lat = destination.lat - self.lat  # delta y

        return sqrt((delta_lon ** 2) + (delta_lat ** 2))
