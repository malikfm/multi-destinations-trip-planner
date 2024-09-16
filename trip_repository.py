import sqlite3
from contextlib import closing
from typing import List, Optional, Tuple

import config


class TripRepository:
    def __init__(self):
        # Create SQLite object in repository (SQLite objects created in a thread can only be used in that same thread).
        self.conn = sqlite3.connect(config.SQLITE_DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def get_hotels(self) -> List[sqlite3.Row]:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT id, name, latitude, longitude FROM hotels")
            return cursor.fetchall()

    def get_hotel_by_id(self, hotel_id: int) -> Optional[sqlite3.Row]:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                "SELECT id, name, latitude, longitude FROM hotels WHERE id = ?",
                (hotel_id,),
            )
            return cursor.fetchone()

    def get_tourism_spots_by_tag(self, tag: str) -> List[sqlite3.Row]:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                """
                SELECT ts.id, ts.name, ts.latitude, ts.longitude
                FROM tourism_spots ts
                JOIN tourism_spots_tags tst ON ts.id = tst.tourism_spot_id
                JOIN tags t ON tst.tag_id = t.id
                WHERE t.name = ?
                """,
                (tag,),
            )
            return cursor.fetchall()

    def get_tags(self) -> List[sqlite3.Row]:
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT name FROM tags")
            return cursor.fetchall()
