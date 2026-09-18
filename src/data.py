import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/app"

engine = create_engine(DATABASE_URL)

df = pd.read_csv("data/gold/gold_data.csv")

df.to_sql(
    "weather",
    engine,
    if_exists="append",
    index=False
)

print("Données chargées dans PostgreSQL")