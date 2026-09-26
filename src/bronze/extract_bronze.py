import requests
import pandas as pd
import os


BASE_PATH = "/opt/airflow/project"

CITIES_FILE = f"{BASE_PATH}/data/bronze/ma.csv"
OUTPUT_FILE = f"{BASE_PATH}/data/bronze/meteo_api.json"

API_URL = "https://api.open-meteo.com/v1/forecast"


def extract():

    cities = pd.read_csv(CITIES_FILE)

    tableaux = []

    for _, row in cities.iterrows():

        ville = row["city"]
        latitude = row["lat"]
        longitude = row["lng"]

        parametres = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": 7,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum,"
                "precipitation_probability_max,"
                "wind_speed_10m_max,"
                "wind_gusts_10m_max,"
                "weather_code"
            ),
            "timezone": "Africa/Casablanca"
        }

        try:

            response = requests.get(
                API_URL,
                params=parametres,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if "daily" not in data:
                raise ValueError("Réponse API invalide : daily absent")

            daily = data["daily"]

            tableau = pd.DataFrame({
                "city": ville,
                "latitude": latitude,
                "longitude": longitude,
                "date": daily["time"],
                "temperature_2m_max": daily["temperature_2m_max"],
                "temperature_2m_min": daily["temperature_2m_min"],
                "precipitation_sum": daily["precipitation_sum"],
                "precipitation_probability_max": daily[
                    "precipitation_probability_max"
                ],
                "wind_speed_10m_max": daily["wind_speed_10m_max"],
                "wind_gusts_10m_max": daily["wind_gusts_10m_max"],
                "weather_code": daily["weather_code"]
            })

            tableaux.append(tableau)

            print(f"Données récupérées pour {ville}")

        except requests.exceptions.Timeout:
            print(f"TIMEOUT : {ville}")

        except requests.exceptions.HTTPError as e:
            print(f"ERREUR HTTP {ville} : {e}")

        except (ValueError, KeyError) as e:
            print(f"ERREUR DONNÉES {ville} : {e}")

        except requests.exceptions.RequestException as e:
            print(f"ERREUR REQUÊTE {ville} : {e}")

    if not tableaux:
        raise Exception("Aucune donnée météo n'a été récupérée.")

    toutes_les_donnees = pd.concat(
        tableaux,
        ignore_index=True
    )

    os.makedirs(
        f"{BASE_PATH}/data/bronze",
        exist_ok=True
    )

    toutes_les_donnees.to_json(
        OUTPUT_FILE,
        orient="records",
        force_ascii=False,
        indent=2
    )

    print(f"Fichier enregistré : {OUTPUT_FILE}")

    return OUTPUT_FILE


if __name__ == "__main__":
    extract()