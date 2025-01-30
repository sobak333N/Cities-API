CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longtitude FLOAT NOT NULL
);

CREATE INDEX idx_city_name ON city USING HASH(name)