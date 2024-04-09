""" DAG to produce test 'california_housing' data to pg  """
from datetime import timedelta

import numpy as np
import pandas as pd
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from sklearn.datasets import fetch_california_housing
from sqlalchemy import create_engine

import logging

from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

DEFAULT_ARGS = {
    "owner": "Dmitrii",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "produce_to_pg",
    tags=["mlops"],
    catchup=False,
    start_date=days_ago(2),
    default_args=DEFAULT_ARGS,
    schedule_interval="@once",
)


def get_engine(conn_id) -> Engine:
    dbhook = BaseHook.get_hook(conn_id=conn_id)
    engine = create_engine(dbhook.get_uri())
    return engine


def produce_to_pg() -> None:
    data = fetch_california_housing()

    dataset = np.concatenate(
        [data["data"], data["target"].reshape([data["target"].shape[0], 1])], axis=1
    )

    dataset = pd.DataFrame(
        dataset, columns=data["feature_names"] + data["target_names"]
    )

    engine = get_engine("pg_connection")

    try:
        dataset.to_sql("california_housing", engine)
        logger.info("Table  'california_housing' created ")
    except ValueError:
        logger.info("Table 'california_housing' already exists")


t1 = PythonOperator(
    task_id="Produce_housing_data_to_pg",
    provide_context=True,
    python_callable=produce_to_pg,
    dag=dag,
)
