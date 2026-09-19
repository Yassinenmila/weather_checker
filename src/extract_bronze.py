import json
import requests
import pandas as pd
import os

csv = pd.read_csv("data/bronze/ma.csv")

tableaux = []

if "meteo_api.json" not in os.listdir('data/bronze'):
    for _, r in csv.iterrows():

        ville = r["city"]
        latitude = r["lat"]
        longitude = r["lng"]

        parametres = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": 7,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max,wind_gusts_10m_max,precipitation_probability_max",
            "timezone": "Africa/Casablanca",
        }

        try:
            reponse = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params=parametres,
                timeout=10
            )

            reponse.raise_for_status()

            donnees = reponse.json()["daily"]

            tableau = pd.DataFrame({
                "city": ville,
                "date": donnees["time"],
                "temperature_max": donnees["temperature_2m_max"],
                "temperature_min": donnees["temperature_2m_min"],
                "precipitation_sum": donnees["precipitation_sum"],
                "weather_code": donnees["weather_code"],
                "wind_speed_max": donnees["wind_speed_10m_max"],
                "wind_gusts_max": donnees["wind_gusts_10m_max"],
                "precipitation_probability_max": donnees["precipitation_probability_max"],
            })

            tableaux.append(tableau)

            print("Données récupérées pour", ville)

        except Exception as e:
            print(f"ERREUR {ville} : {e}")

    toutes_les_donnees = pd.concat(tableaux, ignore_index=True)

    toutes_les_donnees.to_json(
        "data/bronze/meteo_api.json",
        orient="records",
        force_ascii=False,
        indent=2
    )

    print("Fichier meteo_api.json enregistré.")
else:
    print('fichier deja exists')