import os
import pandas as pd


def categorie_temp(temp):

    if temp < 10:
        return "froid"

    elif temp < 20:
        return "frais"

    elif temp < 30:
        return "normal"

    elif temp < 40:
        return "chaud"

    else:
        return "tres chaud"


def categorie_pres(pres):

    if pres == 0:
        return "aucune"

    elif pres < 5:
        return "faible"

    elif pres < 20:
        return "moderee"

    else:
        return "forte"


def categorie_vent(vent):

    if vent < 20:
        return "faible"

    elif vent < 40:
        return "modere"

    elif vent < 60:
        return "fort"

    else:
        return "tres fort"


def temperature_score(temp):

    if 10 <= temp <= 30:
        return 0

    elif 5 <= temp < 10 or 30 < temp <= 35:
        return 30

    elif 0 <= temp < 5 or 35 < temp <= 40:
        return 70

    else:
        return 100


def score_precipitation(pluie):

    if pluie == 0:
        return 0

    elif pluie < 5:
        return 25

    elif pluie < 20:
        return 60

    else:
        return 100


def vent_score(vent):

    if vent < 20:
        return 0

    elif vent < 40:
        return 30

    elif vent < 60:
        return 70

    else:
        return 100


def score_probabilite(prob):

    if prob < 20:
        return 0

    elif prob < 50:
        return 30

    elif prob < 80:
        return 70

    else:
        return 100


def categorie_risque(score):

    if score < 25:
        return "Faible"

    elif score < 50:
        return "Modéré"

    elif score < 75:
        return "Élevé"

    else:
        return "Très élevé"


def transform():

    df = pd.read_csv(
        "/opt/airflow/project/data/silver/silver_weather.csv"
    )

    df["categorie_temperature"] = (
        df["temperature_max"].apply(categorie_temp)
    )

    df["categorie_precipitation"] = (
        df["precipitation_sum"].apply(categorie_pres)
    )

    df["categorie_wind"] = (
        df["wind_speed_max"].apply(categorie_vent)
    )

    df["temperature_score"] = (
        df["temperature_max"].apply(temperature_score)
    )

    df["precipitation_score"] = (
        df["precipitation_sum"].apply(score_precipitation)
    )

    df["probability_score"] = (
        df["precipitation_probability_max"].apply(score_probabilite)
    )

    df["wind_score"] = (
        df["wind_speed_max"].apply(vent_score)
    )

    df["risk_score"] = (
        df["temperature_score"] * 0.20
        + df["precipitation_score"] * 0.30
        + df["probability_score"] * 0.20
        + df["wind_score"] * 0.30
    )

    df["risk_score"] = df["risk_score"].round(2)

    df["risk_category"] = (
        df["risk_score"].apply(categorie_risque)
    )

    output_path = "/opt/airflow/project/data/gold/gold_data.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("Gold créé avec succès")

    return output_path


if __name__ == "__main__":
    transform()