from models.place import Place
from planner import Planner

sample_places = [
    Place("New York", 40.7128, -74.0060),
    Place("Los Angeles", 34.0522, -118.2437),
    Place("Chicago", 41.8781, -87.6298),
    Place("Houston", 29.7604, -95.3698),
    Place("Phoenix", 33.4484, -112.0740)
]

planner = Planner(sample_places)
itinerary = planner.generate_plan("New York", ["Los Angeles", "Chicago", "Houston", "Phoenix"])
print("Optimal Itinerary:", " -> ".join(itinerary))
