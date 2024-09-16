import json
import sqlite3
from contextlib import closing
from typing import Tuple, List

import config


def create_sqlite_tables(cursor) -> None:
    with open("ddl.sql") as f:
        create_stmt = f.read()

    cursor.executescript(create_stmt)


def insert_hotels_to_sqlite(cursor) -> None:
    with open("hotels.json") as f:
        hotels = json.loads(f.read())

    hotels = [str((hotel["name"], hotel["longitude"], hotel["latitude"])) for hotel in hotels]
    values = ",".join(hotels)

    insert_stmt = f"""
        DELETE FROM hotels;
        DELETE FROM sqlite_sequence WHERE name='hotels';
        INSERT INTO hotels (name, longitude, latitude)
        VALUES
        {values}
    """

    cursor.executescript(insert_stmt)


def insert_tags_to_sqlite(cursor):
    insert_stmt = """
        DELETE FROM tags;
        DELETE FROM sqlite_sequence WHERE name='tags';
        INSERT INTO tags (name)
        VALUES
        ("Nature"),
        ("Culture/Heritage"),
        ("Shopping/Culinary")
    """
    return cursor.executescript(insert_stmt)


def insert_tourism_spots_to_sqlite(conn, cursor) -> None:
    # Read tourism spots JSON file.
    with open("tourism_spots.json") as f:
        tourism_spots = json.loads(f.read())

    # Truncate tables.
    clear_tables = """
        DELETE FROM tourism_spots;
        DELETE FROM tourism_spots_tags;
        DELETE FROM sqlite_sequence WHERE name='tourism_spots';
        DELETE FROM sqlite_sequence WHERE name='tourism_spots_tags';
    """
    cursor.executescript(clear_tables)

    # Select tags db. Will be used to map tags from JSON file with the corresponding ids.
    select_tags_stmt = """
        SELECT id, name from tags
    """
    cursor.execute(select_tags_stmt)
    inserted_tags: List[Tuple[int, str]] = cursor.fetchall()

    # Insert tourism spots and their relations with tags (tourism_spots_tags table).
    tourism_spot_insert_stmt = """
        INSERT INTO tourism_spots (name, longitude, latitude)
        VALUES
        {value}
        RETURNING id
    """
    tourism_spot_tags_insert_stmt = """
        INSERT INTO tourism_spots_tags (tourism_spot_id, tag_id)
        VALUES
        {values}
    """
    for tourism_spot in tourism_spots:
        # Insert a tourism spot data and return its ID.
        tourism_spot_value = (tourism_spot["name"], tourism_spot["longitude"], tourism_spot["latitude"])
        inserted_tourism_spot_id = cursor.execute(tourism_spot_insert_stmt.format(value=tourism_spot_value)).fetchone()[0]
        conn.commit()

        # Insert relations between a tourism spot and its tags.
        tourism_spot_tags_values = [
            str((inserted_tourism_spot_id, inserted_tag[0]))
            for tag_name in tourism_spot["tags"]
            for inserted_tag in inserted_tags if tag_name == inserted_tag[1]
        ]
        tourism_spot_tags_values = ",".join(tourism_spot_tags_values)
        cursor.executescript(tourism_spot_tags_insert_stmt.format(values=tourism_spot_tags_values))


if __name__ == "__main__":
    with closing(sqlite3.connect(config.SQLITE_DB_PATH)) as conn:
        with closing(conn.cursor()) as cursor:
            print("Creating tables.")
            create_sqlite_tables(cursor)
            print("Finished.")

            print("Inserting hotels.")
            insert_hotels_to_sqlite(cursor)
            print("Finished.")

            print("Inserting tags.")
            insert_tags_to_sqlite(cursor)
            print("Finished.")

            print("Inserting tourism spots.")
            insert_tourism_spots_to_sqlite(conn, cursor)
            print("Finished.")
