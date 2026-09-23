import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Weather Checker",
    layout="wide"
)

st.title("Weather Checker")

st.write("Dashboard de surveillance des risques météorologiques")

DATABASE_URL = "postgresql+psycopg2://postgres:admin@postgres:5432/app"

engine = create_engine(DATABASE_URL)

df = pd.read_sql("SELECT * FROM weather", engine)


col1, col2, col3 = st.columns(3)

col1.metric("Villes", df["city"].nunique())

col2.metric("Risque moyen", round(df["risk_score"].mean(), 2))

col3.metric("Risque maximum", round(df["risk_score"].max(), 2))



col4, col5 = st.columns(2)

col4.metric(
    "Température maximale",
    f"{df['temperature_max'].max():.1f} °C"
)

col5.metric(
    "Précipitations maximales",
    f"{df['precipitation_sum'].max():.1f} mm"
)


ville = st.selectbox(
    "Ville",
    ["Toutes"] + sorted(df["city"].unique())
)

if ville != "Toutes":
    df = df[df["city"] == ville]



risque = st.selectbox(
    "Niveau de risque",
    ["Tous"] + sorted(df["risk_category"].unique())
)

if risque != "Tous":
    df = df[df["risk_category"] == risque]


st.subheader(" Où faut-il être particulièrement vigilant ?")

if not df.empty:

    ligne_risque = df.loc[df["risk_score"].idxmax()]

    st.warning(
        f"Risque maximal à **{ligne_risque['city']}** "
        f"le **{ligne_risque['date']}** "
        f"avec un score de **{ligne_risque['risk_score']}/100** "
        f"({ligne_risque['risk_category']})."
    )


st.subheader("Risque moyen par ville")

risque_ville = (
    df.groupby("city")["risk_score"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(risque_ville)



st.subheader("Température maximale par ville")

temperature_ville = (
    df.groupby("city")["temperature_max"]
    .max()
    .sort_values(ascending=False)
)

st.bar_chart(temperature_ville)


st.subheader("Précipitations maximales par ville")

precipitation_ville = (
    df.groupby("city")["precipitation_sum"]
    .max()
    .sort_values(ascending=False)
)

st.bar_chart(precipitation_ville)



st.subheader("Risque maximal par période")

risque_date = (
    df.groupby("date")["risk_score"]
    .max()
)

st.line_chart(risque_date)


st.subheader("Prévisions météorologiques")

st.dataframe(df)