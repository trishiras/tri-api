from pymongo import MongoClient
from tri_api.core.logger import logger
from tri_api.support.enums import MongoOption


def connect_to_mongodb():
    """Establish connection to MongoDB"""
    try:
        logger.info("Connecting to MongoDB...")
        client = MongoClient(
            f"mongodb://{MongoOption.username.value}:{MongoOption.password.value}@{MongoOption.host.value}:{MongoOption.port.value}/",
            serverSelectionTimeoutMS=5000,  # 5 second timeout
        )

        # Test connection
        client.server_info()
        logger.info("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return None
