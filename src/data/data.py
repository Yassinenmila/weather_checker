import pandas as pd
from sqlalchemy import create_engine


def load_postgres(gold_path):

    DATABASE_URL = "postgresql+psycopg2://postgres:admin@postgres:5432/app"

    engine = create_engine(DATABASE_URL)

    cities = pd.read_csv("data/bronze/ma.csv")

    cities = cities[
        ["city", "lat", "lng"]
    ]

    cities.to_sql(
        "cities",
        engine,
        if_exists="replace",
        index=False
    )

    df = pd.read_csv(gold_path)

    df.to_sql(
        "weathers",
        engine,
        if_exists="replace",
        index=False
    )

    print("Données chargées dans PostgreSQL")