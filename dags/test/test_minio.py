"""DAG to functional test amazon S3 """
from datetime import timedelta
from random import randint

import backoff
from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import logging

from airflow.utils.dates import days_ago
from botocore.exceptions import (
    ConnectTimeoutError,
    EndpointConnectionError,
    ConnectionError,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

cid = "s3_connection"

DEFAULT_ARGS = {
    "owner": "Dmitrii",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "test_local_minio",
    tags=["mlops"],
    catchup=False,
    start_date=days_ago(2),
    default_args=DEFAULT_ARGS,
    schedule_interval="@once",
)

rand = randintrand = randint(1, 1000)


def give_up_connection() -> None:
    logger.error(f"Failed to connect to db  . Please check connect options or host")


@backoff.on_exception(
    backoff.expo,
    (EndpointConnectionError, ConnectionError, ConnectTimeoutError),
    max_time=60,
    max_tries=3,
    on_giveup=give_up_connection,
)
def write_text_file() -> None:
    with open(f"/tmp/test.txt", "w") as fp:
        test = f"test"
        # Add file generation/processing step here, E.g.:
        fp.write(test)

        # Upload generated file to Minio
        s3 = S3Hook(
            cid,
            transfer_config_args={
                "use_threads": False,
            },
        )
        s3.load_file(
            "/tmp/test.txt", key=f"my-test-file{rand}.txt", bucket_name="airflow"
        )

        logger.info("File loaded")


def delete_text_file() -> None:
    s3 = S3Hook(
        cid,
        transfer_config_args={
            "use_threads": False,
        },
    )
    # Delete generated file from Minio
    s3.delete_objects(bucket="airflow", keys=f"my-test-file{rand}.txt")

    logger.info("file deleted")


# Create a task to call your processing function
t1 = PythonOperator(
    task_id="generate_and_upload_to_s3",
    provide_context=True,
    python_callable=write_text_file,
    dag=dag,
)

t2 = PythonOperator(
    task_id="delete_from_s3",
    provide_context=True,
    python_callable=delete_text_file,
    dag=dag,
)

t1 >> t2
