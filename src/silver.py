import pandas as pd
import os

def verifier(df):

    if df.isnull().any().any():
        print("Il y a des valeurs nulles")

    elif df.duplicated(subset=["city", "date"]).any():
        print("Il y a des doublons")

    elif (df["temperature_min"] > df["temperature_max"]).any():
        print("Valeur illogique dans température min/max")

    elif (
        (df["precipitation_probability_max"] < 0).any()
        or
        (df["precipitation_probability_max"] > 100).any()
    ):
        print("Valeur illogique dans precipitation_probability_max")

    elif (df["precipitation_sum"] < 0).any():
        print("Impossible que la précipitation soit négative")

    elif (df["wind_speed_max"] < 0).any():
        print("Impossible que la vitesse du vent soit négative")

    elif (df["wind_gusts_max"] < 0).any():
        print("Impossible que les rafales soient négatives")

    else:
        return True

if 'silver_weather.csv' not in os.listdir('data/silver'):
    df = pd.read_json("data/bronze/meteo_api.json")


    df["city"] = df["city"].astype("string")
    df["date"] = pd.to_datetime(df["date"])


    columns = [
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
        "precipitation_probability_max",
        "wind_speed_max",
        "wind_gusts_max",
        "weather_code"
    ]

    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")


    if verifier(df) is True:

        df.to_csv(
            "data/silver/silver_weather.csv",
            index=False
        )

        print("Silver créé avec succès")
else: 
    print('fishier deja exist !!')