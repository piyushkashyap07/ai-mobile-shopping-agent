from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    client: MongoClient = None
    db: Database = None

    @classmethod
    def connect_to_mongodb(cls):
        """Connect to MongoDB if not already connected"""
        if cls.client is None:
            try:
                cls.client = MongoClient(settings.MONGODB_URI, tlsAllowInvalidCertificates=True)
                cls.db = cls.client[settings.MONGODB_DB_NAME]
                logger.info(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise e

    @classmethod
    def close_mongodb_connection(cls):
        """Close MongoDB connection"""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None
            logger.info("MongoDB connection closed")

    @classmethod
    def get_collection(cls, collection_name: str) -> Collection:
        """Get a collection from the database"""
        if cls.db is None:
            print("Connecting to MongoDB")
            cls.connect_to_mongodb()
        return cls.db[collection_name]

# Singleton instance
mongodb = MongoDB() 