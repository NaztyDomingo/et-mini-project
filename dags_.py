from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

import os
import requests
from datetime import datetime
import json
import pandas as pd
import configparser







with DAG(
    "weather_dag",
    start_date=datetime(2021, 1, 1), schedule="@hourly", 
    catchup=False
):
    API_Download = PythonOperator(
        task_id="API\Download",
        python_callable=_API_Download
    )

    raw = BranchPythonOperator(
        task_id="Raw",
        python_callable=_Raw
    )

    harmonized = PythonOperator(
        task_id="Harmonized",
        python_callable=_Harmonized
    )

    cleansed = PythonOperator(
        task_id="Cleansed",
        python_callable=_cleansed
    )

    staged = PythonOperator(
        task_id="Staged",
        python_callable=_staged
    )

    modelled = PythonOperator(
        task_id="Modelled",
        python_callable=_modelled
    )

    API_Download >> raw >> harmonized >> cleansed >> staged >> modelled
