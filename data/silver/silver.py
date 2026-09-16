from ..bronze import csv
import pandas as pd

data_csv = csv

df_ville=pd.DataFrame(csv)

df_meteo=pd.read_json("data/bronze/meteo_api.json")

df_ville.columns=df_ville.columns.str.lower().str.strip()
df_meteo.columns=df_meteo.columns.str.lower().str.strip()
df_ville['city']=df_ville["city"].str.title()
df_ville.drop(columns=["capital","iso2","admin_name","population","population_proper","country"],inplace=True)

df_meteo.drop(columns=['generationtime_ms','utc_offset_seconds','timezone','timezone_abbreviation','elevation','location_id','daily_units'],inplace=True)

df_ville["lat"] = pd.to_numeric(df_ville["lat"], errors="coerce")
df_ville["lng"] = pd.to_numeric(df_ville["lng"], errors="coerce")

