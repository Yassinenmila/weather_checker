# import json 
# import requests
# import pandas as pd
# import numpy as np

# csv = pd.read_csv('data/bronze/ma.csv')


# meteo=[]

# for i , r in csv.iterrows():
#     lat,lng=r['lat'],r['lng']
#     url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto"

#     try:
#         res=requests.get(url,timeout=10)
#         if res.status_code==200:
#             meteo.append(
#                 {"ville":r["city"], "meteo":res.json()}
#             )

#     except Exception as e:
#         print(f"erreur {r['city']}: {e}")

# with open("data/bronze/meteo_api.json", "w", encoding="utf-8") as f:
#     json.dump(meteo, f, ensure_ascii=False, indent=2)


import json
import pandas as pd
import requests

csv = pd.read_csv("data/bronze/ma.csv")

lats = ",".join(csv["lat"].astype(str))
lngs = ",".join(csv["lng"].astype(str))

url = "https://api.open-meteo.com/v1/forecast?"


parametres = {
        "latitude": lats,
        "longitude": lngs,
        "past_days": 7,
        "forecast_days": 7,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max,wind_gusts_10m_max,precipitation_probability_max",
        "timezone": "Africa/Casablanca",
    }

try:
    res = requests.get(url, params=parametres, timeout=30)

    if res.status_code == 200:

        meteo_data = res.json()

        with open("data/bronze/meteo_api.json", "w", encoding="utf-8") as f:
         json.dump(meteo_data, f, ensure_ascii=False, indent=2)
    else:
       print('there is a problem !!!')
except Exception as e:
    print(f'ERREUR !!!! : {e} ')