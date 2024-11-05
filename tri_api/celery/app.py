import asyncio
import nest_asyncio
from celery import Celery
from typing import Dict, Any
from kombu import Exchange, Queue
from tri_api.core.logger import logger
from tri_api.rabbitmq.connections import create_rabbitmq_url
from celery.signals import (
    worker_ready,
    worker_shutdown,
    worker_process_init,
)


class CeleryConfig:
    """Centralized configuration class for Celery settings"""

    # Broker settings
    broker_url = create_rabbitmq_url()
    broker_connection_retry = True
    broker_connection_max_retries = 5
    broker_heartbeat = 0
    broker_pool_limit = 10

    # Result backend settings
    result_backend = "rpc://"
    result_expires = 60 * 60 * 24

    # Serialization settings
    accept_content = ["json"]
    result_serializer = "json"
    task_serializer = "json"

    # Define the exchange
    task_default_exchange = "tri"
    task_default_exchange_type = "direct"

    # Define the default queue
    task_default_queue = "tri"
    task_default_routing_key = "tri"

    # Define queue Task queues with explicit settings
    task_queues = {
        Queue(
            name="tri",
            exchange=Exchange(
                "tri",
                type="direct",
                durable=True,
            ),
            routing_key="tri",
            queue_arguments={
                "x-max-priority": 10,
                "durable": True,
            },
        ),
    }

    # Explicitly define task routes
    task_routes = {
        "tri_api.celery.tasks.*": {
            "queue": "tri",
            "exchange": "tri",
            "routing_key": "tri",
        },
    }

    # Time settings
    enable_utc = True
    timezone = "Asia/Kolkata"

    # Task execution settings
    task_acks_late = True
    task_reject_on_worker_lost = True
    task_time_limit = 900
    task_soft_time_limit = 600

    # Worker settings
    worker_prefetch_multiplier = 1
    worker_concurrency = 4
    worker_max_tasks_per_child = 1000

    # Retry settings
    task_default_retry_delay = 180
    task_max_retries = 3

    # Pool settings - Using solo pool for better async support
    worker_pool = "solo"


def create_celery_app() -> Celery:
    """Create and configure the Celery application"""
    logger.info("Started creating tri celery app")

    app = Celery("tri_api_celery_app")
    app.config_from_object(CeleryConfig)
    app.autodiscover_tasks(["tri_api.celery.tasks"])

    # Declare queue on startup
    with app.connection() as connection:
        channel = connection.channel()

        # Declare exchange
        exchange = Exchange(
            "tri",
            type="direct",
            durable=True,
        )
        exchange(channel).declare()

        # Declare queue
        queue = Queue(
            "tri",
            exchange=exchange,
            routing_key="tri",
            queue_arguments={
                "x-max-priority": 10,
                "durable": True,
            },
        )
        queue(channel).declare()

    return app


@worker_process_init.connect
def init_worker_process(*args: Any, **kwargs: Dict[str, Any]) -> None:
    """Initialize the event loop for each worker process"""
    logger.info("Initializing worker process with event loop")
    try:
        loop = asyncio.get_event_loop()
        logger.info("Got existing event loop")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        logger.info("Created new event loop")

    # Enable nested event loops
    nest_asyncio.apply()
    logger.info("Applied nest_asyncio")


@worker_ready.connect
def on_worker_ready(sender: Any, **kwargs: Dict[str, Any]) -> None:
    """Handler for worker ready signal"""
    logger.info(f"Celery worker {sender.hostname} is ready")


@worker_shutdown.connect
def on_worker_shutdown(sender: Any, **kwargs: Dict[str, Any]) -> None:
    """Handler for worker shutdown signal"""
    logger.info(f"Celery worker {sender.hostname} is shutting down")


def async_to_sync(func):
    """Decorator to convert async functions to sync for Celery tasks"""
    from functools import wraps

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            return loop.run_until_complete(func(*args, **kwargs))
        except Exception as e:
            logger.error(f"Error in async task: {str(e)}")
            raise

    return wrapped


tri_api_celery_app = create_celery_app()
logger.info("Finished creating tri celery app")
