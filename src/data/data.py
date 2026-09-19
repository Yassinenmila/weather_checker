import pandas as pd

from sqlalchemy import create_engine


def load_postgres(gold_path):

    DATABASE_URL = "postgresql+psycopg2://postgres:postgres@postgres:5432/app"

    engine = create_engine(DATABASE_URL)

    df = pd.read_csv(gold_path)

    df.to_sql(
        "weather",
        engine,
        if_exists="append",
        index=False
    )

    print("Données chargées dans PostgreSQL")