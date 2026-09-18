CREATE TABLE IF NOT EXISTS weather_forecasts (
    id SERIAL PRIMARY KEY,

    city VARCHAR(100) NOT NULL,
    date DATE NOT NULL,

    temperature_max FLOAT,
    temperature_min FLOAT,
    precipitation_sum FLOAT,
    weather_code INTEGER,
    wind_speed_max FLOAT,
    wind_gusts_max FLOAT,
    precipitation_probability_max FLOAT,

    categorie_temperature VARCHAR(50),
    categorie_presipitation VARCHAR(50),
    categorie_wind VARCHAR(50),

    temperature_score FLOAT,
    precipitation_score FLOAT,
    probability_score FLOAT,
    wind_score FLOAT,

    risk_score FLOAT,
    risk_category VARCHAR(50),

    UNIQUE(city, date)
);