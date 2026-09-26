import pandas as pd
import os


def verifier(df):

    if df.isnull().any().any():
        print("Il y a des valeurs nulles")
        return False

    if df.duplicated(subset=["city", "date"]).any():
        print("Il y a des doublons")
        return False

    if (df["temperature_min"] > df["temperature_max"]).any():
        print("Valeur illogique dans température min/max")
        return False

    if (
        (df["precipitation_probability_max"] < 0).any()
        or
        (df["precipitation_probability_max"] > 100).any()
    ):
        print("Valeur illogique dans precipitation_probability_max")
        return False

    if (df["precipitation_sum"] < 0).any():
        print("Impossible que la précipitation soit négative")
        return False

    if (df["wind_speed_max"] < 0).any():
        print("Impossible que la vitesse du vent soit négative")
        return False

    if (df["wind_gusts_max"] < 0).any():
        print("Impossible que les rafales soient négatives")
        return False

    return True


def clean():

    df = pd.read_json("data/bronze/meteo_api.json")

    df["city"] = df["city"].astype("string")

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    columns = [
        "latitude",
        "longitude",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "precipitation_probability_max",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "weather_code"
    ]

    for column in columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.rename(columns={
        "temperature_2m_max": "temperature_max",
        "temperature_2m_min": "temperature_min",
        "wind_speed_10m_max": "wind_speed_max",
        "wind_gusts_10m_max": "wind_gusts_max"
    })

    if verifier(df):

        output_path = "data/silver/silver_weather.csv"

        df.to_csv(
            output_path,
            index=False
        )

        print("Silver créé avec succès")

        return output_path

    else:

        raise ValueError(
            "Les données Silver ne passent pas les contrôles de qualité."
        )


if __name__ == "__main__":
    clean()