from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: MongoClient = None
    connected: bool = False
    
db = Database()

async def get_database():
    """Dependency to get database connection"""
    if not db.connected or not db.client:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail="Database is not available. Please ensure MongoDB is running and accessible."
        )
    return db.client[settings.database_name]

async def connect_to_mongo():
    """Connect to MongoDB with error handling"""
    try:
        db.client = MongoClient(
            settings.mongodb_url,
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000
        )
        # Test connection
        db.client.admin.command('ping')
        db.connected = True
        logger.info("✅ Connected to MongoDB")
        print("✅ Connected to MongoDB")
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        db.connected = False
        logger.warning(f"⚠️  Could not connect to MongoDB: {e}")
        logger.warning(f"⚠️  MongoDB URL: {settings.mongodb_url}")
        logger.warning("⚠️  The application will start but database operations will fail.")
        print(f"⚠️  Warning: Could not connect to MongoDB at {settings.mongodb_url}")
        print("⚠️  Please ensure MongoDB is running. The app will start but database features won't work.")
    except Exception as e:
        db.connected = False
        logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
        print(f"❌ Error connecting to MongoDB: {e}")

async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        try:
            db.client.close()
            logger.info("❌ Closed MongoDB connection")
            print("❌ Closed MongoDB connection")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
    db.connected = False
