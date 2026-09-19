import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Weather Checker",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Checker")
st.write("Dashboard de surveillance des risques météorologiques")

DATABASE_URL = "postgresql+psycopg2://postgres:admin@postgres:5432/app"
engine = create_engine(DATABASE_URL)

df = pd.read_sql("SELECT * FROM weather", engine)

col1, col2, col3 = st.columns(3)

col1.metric("Villes", df["city"].nunique())
col2.metric("Risque moyen", round(df["risk_score"].mean(), 2))
col3.metric("Risque maximum", round(df["risk_score"].max(), 2))

ville = st.selectbox(
    "Ville",
    ["Toutes"] + sorted(df["city"].unique())
)

if ville != "Toutes":
    df = df[df["city"] == ville]

st.subheader("Prévisions météorologiques")
st.dataframe(df)