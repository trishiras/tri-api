import random
import requests
import traceback
from boto3.session import Session
from botocore.config import Config
from urllib3.util.retry import Retry
from tri_api.core.logger import logger
from requests.adapters import HTTPAdapter
from botocore.exceptions import ClientError
from tri_api.support.enums import USER_AGENTS, AWSOption
from requests.exceptions import (
    RequestException,
    Timeout,
    HTTPError,
    ConnectionError,
)


def create_aws_client(service: str):
    config = Config(
        read_timeout=360,
        connect_timeout=360,
    )
    session = Session(
        aws_access_key_id=AWSOption.access_key.value,
        aws_secret_access_key=AWSOption.secret_key.value,
        region_name=AWSOption.region.value,
    )
    client = session.client(
        service,
        config=config,
    )
    return client


def create_presigned_link(
    object_name: str,
    expiration: int = 3600,
):
    client = create_aws_client("s3")
    try:
        response = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": AWSOption.s3_bucket.value,
                "Key": object_name,
            },
            ExpiresIn=expiration,
        )
    except ClientError as err:
        logger.error(err)
        logger.debug(traceback.format_exc())
        return None
    return response


def scrape(
    url: str,
    headers: dict = None,
    payload: dict = None,
    schema: str = "https",
    randomize: bool = True,
    post_request: bool = False,
    timeout: int = 10,
    retry: bool = True,
    retries: int = 5,
    backoff_factor: float = 1.0,
    allowed_status_forcelist: list = None,
) -> requests.Response:
    """
    Scrape a URL using GET or POST requests with optional retries, timeouts, and random user agents.

    Args:
        url (str): The target URL.
        headers (dict): Optional headers to include in the request.
        payload (dict): Optional JSON payload for POST requests.
        schema (str): The schema to use, either 'http' or 'https'. Default is 'https'.
        randomize (bool): Whether to randomize the User-Agent header. Default is True.
        post_request (bool): Whether to use a POST request. Default is True.
        timeout (int): The timeout for the request in seconds. Default is 10.
        retry (bool): Whether to retry on failure. Default is True.
        retries (int): Number of retries. Default is 5.
        backoff_factor (float): The backoff factor for retries. Default is 1.0.
        allowed_status_forcelist (list): List of status codes that trigger a retry. Default is [403, 502, 503, 504].

    Returns:
        requests.Response: The response object, or None if the request fails.
    """
    response = None
    session = requests.Session()

    if allowed_status_forcelist is None:
        allowed_status_forcelist = [403, 502, 503, 504]

    try:
        if schema not in ["http", "https"]:
            raise ValueError("Invalid schema, must be 'http' or 'https'")

        if randomize and USER_AGENTS:
            user_agent = random.choice(USER_AGENTS)
            session.headers.update({"User-Agent": user_agent})

        if headers:
            session.headers.update(headers)

        if retry:
            retry_strategy = Retry(
                total=retries,
                backoff_factor=backoff_factor,
                status_forcelist=allowed_status_forcelist,
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount(f"{schema}://", adapter)

        logger.info(f"Making {'POST' if post_request else 'GET'} request to {url}")

        if post_request:
            response = session.post(
                url,
                headers=headers,
                json=payload,
                timeout=timeout,
            )
        else:
            response = session.get(
                url,
                headers=headers,
                timeout=timeout,
            )

        response.raise_for_status()

        logger.info(f"Response received with status code: {response.status_code}")

    except Timeout:
        logger.error(f"Request timed out after {timeout} seconds: {url}")
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - URL: {url}")
    except ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err} - URL: {url}")
    except RequestException as req_err:
        logger.error(f"Request error: {req_err} - URL: {url}")
        logger.debug(traceback.format_exc())
    except ValueError as val_err:
        logger.error(f"Value error: {val_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        logger.debug(traceback.format_exc())

    return response
