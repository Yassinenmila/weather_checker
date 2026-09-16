
import pandas as pd




df=pd.read_json("data/bronze/meteo_api.json")


print(df.duplicated().sum())