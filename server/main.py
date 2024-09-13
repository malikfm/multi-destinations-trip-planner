import os
import sqlite3
from contextlib import closing

import config

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/hotels")
def get_hotels():
    print(os.getcwd())
    print(config.SQLITE_DB_PATH)
    with closing(sqlite3.connect(config.SQLITE_DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as cursor:
            rows = cursor.execute("SELECT id, name FROM hotels").fetchall()

    return [dict(row) for row in rows]


def get_point_of_interests():
    # get by cat from all tourism spots
    return


# hotel -> select tourism spots point of interests
# -> calculate initial (hotel) goals (point of interests)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
