from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def extract():
    print("🚀 Extraction Bronze")


def silver():
    print("🧹 Transformation Silver")


def gold():
    print("📊 Transformation Gold")


def load_postgres():
    print("🐘 Chargement PostgreSQL")


with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 9, 19),
    schedule="0 8 * * *",
    catchup=False,
) as dag:

    task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    task_silver = PythonOperator(
        task_id="silver",
        python_callable=silver,
    )

    task_gold = PythonOperator(
        task_id="gold",
        python_callable=gold,
    )

    task_load = PythonOperator(
        task_id="load_postgres",
        python_callable=load_postgres,
    )

    task_extract >> task_silver >> task_gold >> task_load