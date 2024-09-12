CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE IF NOT EXISTS tourism_spots (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tourism_spots_tags (
    id INTEGER PRIMARY KEY,
    tourism_spot_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY(tourism_spot_id) REFERENCES tourism_spots(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);
