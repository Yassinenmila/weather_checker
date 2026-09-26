import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


# Configuration
st.set_page_config(
    page_title="Weather Risk Dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Risk Dashboard")
st.write("Prévisions météo et analyse des risques pour les livraisons")


# Connexion PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:admin@postgres:5432/app"

engine = create_engine(DATABASE_URL)


# Lire les données
cities = pd.read_sql(
    "SELECT * FROM cities",
    engine
)

forecasts = pd.read_sql(
    "SELECT * FROM weathers",
    engine
)


# Convertir la date
forecasts["date"] = pd.to_datetime(forecasts["date"])


# =========================
# FILTRES
# =========================

st.sidebar.header("🔎 Filtres")

# Filtre ville
city_list = ["Toutes"] + sorted(forecasts["city"].unique().tolist())

selected_city = st.sidebar.selectbox(
    "Ville",
    city_list
)


# Filtre période
period = st.sidebar.selectbox(
    "Période",
    ["Toutes", "Aujourd'hui", "Prochains 3 jours", "Prochains 7 jours"]
)


# Filtre niveau de risque
risk_list = [
    "Tous",
    "Faible",
    "Modéré",
    "Élevé",
    "Très élevé"
]

selected_risk = st.sidebar.selectbox(
    "Niveau de risque",
    risk_list
)


# Filtre date
min_date = forecasts["date"].min().date()
max_date = forecasts["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# =========================
# APPLICATION DES FILTRES
# =========================

filtered = forecasts.copy()


# Ville
if selected_city != "Toutes":
    filtered = filtered[
        filtered["city"] == selected_city
    ]


# Date
if len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered = filtered[
        (filtered["date"] >= start_date)
        & (filtered["date"] <= end_date)
    ]


# Période
if period == "Aujourd'hui":

    today = forecasts["date"].min()

    filtered = filtered[
        filtered["date"] == today
    ]

elif period == "Prochains 3 jours":

    first_day = forecasts["date"].min()
    last_day = first_day + pd.Timedelta(days=2)

    filtered = filtered[
        (filtered["date"] >= first_day)
        & (filtered["date"] <= last_day)
    ]

elif period == "Prochains 7 jours":

    first_day = forecasts["date"].min()
    last_day = first_day + pd.Timedelta(days=6)

    filtered = filtered[
        (filtered["date"] >= first_day)
        & (filtered["date"] <= last_day)
    ]


# Niveau de risque
if selected_risk != "Tous":

    filtered = filtered[
        filtered["risk_category"] == selected_risk
    ]


# =========================
# KPI
# =========================

st.header("📊 Indicateurs clés")


number_cities = filtered["city"].nunique()

max_temperature = filtered["temperature_max"].max()

max_precipitation = filtered["precipitation_sum"].max()

risk_periods = filtered[
    filtered["risk_score"] >= 50
].shape[0]


if len(filtered) > 0:

    highest_risk_row = filtered.loc[
        filtered["risk_score"].idxmax()
    ]

    highest_risk_city = highest_risk_row["city"]

else:

    highest_risk_city = "Aucune donnée"


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "🏙️ Nombre de villes",
    number_cities
)

col2.metric(
    "🌡️ Température maximale",
    f"{max_temperature:.1f} °C" if pd.notna(max_temperature) else "N/A"
)

col3.metric(
    "🌧️ Précipitations maximales",
    f"{max_precipitation:.1f} mm" if pd.notna(max_precipitation) else "N/A"
)

col4.metric(
    "⚠️ Périodes à risque",
    risk_periods
)

col5.metric(
    "📍 Ville à risque",
    highest_risk_city
)


# =========================
# VIGILANCE
# =========================

st.header("⚠️ Où et quand faut-il être vigilant ?")


if len(filtered) > 0:

    highest_risk = filtered.sort_values(
        "risk_score",
        ascending=False
    ).head(10)

    st.dataframe(
        highest_risk[
            [
                "city",
                "date",
                "temperature_max",
                "precipitation_sum",
                "wind_speed_max",
                "risk_score",
                "risk_category"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")


# =========================
# GRAPHIQUE RISQUE
# =========================

st.header("📈 Évolution du risque")


if len(filtered) > 0:

    chart_data = filtered[
        ["date", "risk_score"]
    ].groupby("date").mean()

    st.line_chart(
        chart_data
    )


# =========================
# PREVISIONS
# =========================

st.header("🌦️ Prévisions météo")


if len(filtered) > 0:

    st.dataframe(
        filtered[
            [
                "city",
                "date",
                "temperature_max",
                "temperature_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_max",
                "wind_gusts_max",
                "weather_code",
                "risk_score",
                "risk_category"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )