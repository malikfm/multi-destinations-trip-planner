import sqlite3
from contextlib import closing

import config

with open("./ddl.sql") as f:
    create_tables_stmt = f.read()

with closing(sqlite3.connect(config.SQLITE_DB_PATH)) as conn:
    with closing(conn.cursor()) as cursor:
        cursor.executescript(create_tables_stmt)
