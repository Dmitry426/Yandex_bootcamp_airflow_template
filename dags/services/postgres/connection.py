__all__ = "get_postgres_conn"
import logging

import backoff

from airflow.providers.postgres.hooks.postgres import PostgresHook

from psycopg2 import OperationalError
from psycopg2.extensions import connection

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def give_up_connection() -> None:
    logger.error(
        f"Failed to connect to postgres . Please check connect options or host"
    )


@backoff.on_exception(
    backoff.expo,
    OperationalError,
    max_time=60,
    max_tries=3,
    on_giveup=give_up_connection,
)
def get_postgres_conn(postgres_conn_name) -> connection:
    hook = PostgresHook(postgres_conn_name)
    conn = hook.get_conn()
    return conn
