__all__ = ("get_s3_hook", "get_s3_resource")

import logging
from functools import lru_cache

import backoff

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from boto3.resources.base import ServiceResource

from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
    EndpointConnectionError,
    ParamValidationError,
    ConnectionError,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def give_up_connection() -> None:
    logger.error(f"Failed to connect to s3. Please check connect options or host")


@backoff.on_exception(
    backoff.expo,
    (EndpointConnectionError, ConnectionError, ConnectTimeoutError),
    max_time=60,
    max_tries=3,
    on_giveup=give_up_connection,
)
@lru_cache(maxsize=None)
def get_s3_hook(s3_connection) -> S3Hook:
    """Get s3 hook object . Use cache to make singleton"""
    try:
        return S3Hook(
            s3_connection,
            transfer_config_args={
                "use_threads": False,
            },
        )
    except (ParamValidationError, ClientError) as error:
        logger.error("S3 credentials err")
        raise ValueError(
            "The AWS parameters you provided are incorrect: {}".format(error)
        ) from error


@backoff.on_exception(
    backoff.expo,
    (EndpointConnectionError, ConnectionError, ConnectTimeoutError),
    max_time=60,
    max_tries=3,
    on_giveup=give_up_connection,
)
def get_s3_resource(s3_connection) -> ServiceResource:
    """Interface to  get resource in case we Use real AWS instead of Minio"""
    try:
        s3 = get_s3_hook(s3_connection)
        session = s3.get_session(s3.conn_config.region_name)
        return session.resource("s3", endpoint_url=s3.conn_config.endpoint_url)
    except (ParamValidationError, ClientError) as error:
        logger.error("S3 credentials err")
        raise ValueError(
            "The AWS parameters you provided are incorrect: {}".format(error)
        ) from error
