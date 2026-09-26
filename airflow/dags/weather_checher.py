from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

import sys

sys.path.append("/opt/airflow/project")

from src.bronze import extract
from src.silver import clean
from src.gold import transform
from src.data import load_postgres

def run_load_postgres(**context):

    gold_path = context["ti"].xcom_pull(
        task_ids="gold"
    )

    load_postgres(gold_path)
with DAG(
    dag_id="weather_checher",
    start_date=datetime(2026, 9, 19),
    schedule="@daily",
    catchup=False,
) as dag:

    task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    task_silver = PythonOperator(
        task_id="silver",
        python_callable=clean,
    )

    task_gold = PythonOperator(
        task_id="gold",
        python_callable=transform,
    )

    task_load = PythonOperator(
        task_id="load_postgres",
        python_callable=run_load_postgres,
    )

    task_extract >> task_silver >> task_gold >> task_load