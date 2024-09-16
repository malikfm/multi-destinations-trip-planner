from os import environ as env

SQLITE_DB_PATH = env.get("SQLITE_DB_PATH", "multi_destinations_trip_planner.db")
