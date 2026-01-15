"""
Database connection and session management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class MongoDB:
    """MongoDB connection manager"""
    
    client: AsyncIOMotorClient = None
    db = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Connect to MongoDB"""
    mongodb_url = settings.get_mongodb_url()
    db_name = settings.get_db_name()
    mongodb.client = AsyncIOMotorClient(mongodb_url)
    mongodb.db = mongodb.client[db_name]
    print(f"[OK] Connected to MongoDB: {db_name}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        print("[CLOSED] Closed MongoDB connection")


def get_database():
    """Get database instance"""
    return mongodb.db
