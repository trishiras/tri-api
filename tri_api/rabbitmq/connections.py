from tri_api.core.logger import logger
from tri_api.support.enums import RabbitMQOption


def create_rabbitmq_url():
    """ "Creating RabbitMQ url"""
    rabbitmq_url = ""
    try:
        logger.info("Creating RabbitMQ url")
        rabbitmq_url = f"{RabbitMQOption.schema.value}://{RabbitMQOption.username.value}:{RabbitMQOption.password.value}@{RabbitMQOption.host.value}:{RabbitMQOption.port.value}/{RabbitMQOption.vhost.value}"
    except Exception as e:
        logger.error(f"Error creating rabbitmq url: {e}")

    return rabbitmq_url
