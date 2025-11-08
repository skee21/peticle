from app.storage.json_repository import get_repository, JSONRepository
import logging

logger = logging.getLogger(__name__)

class JSONDatabase:
    def __init__(self, repository: JSONRepository):
        self._repo = repository
    
    @property
    def pets(self):
        return JSONCollection(self._repo, "pets")
    
    @property
    def videos(self):
        return JSONCollection(self._repo, "videos")
    
    @property
    def users(self):
        return JSONCollection(self._repo, "users")
    
    @property
    def products(self):
        return JSONCollection(self._repo, "products")


class JSONCollection:
    def __init__(self, repository: JSONRepository, collection_name: str):
        self._repo = repository
        self._collection = collection_name
    
    async def insert_one(self, document):
        return await self._repo.insert_one(self._collection, document)
    
    async def find(self, query=None):
        return await self._repo.find(self._collection, query)
    
    async def find_one(self, query):
        return await self._repo.find_one(self._collection, query)
    
    async def update_one(self, query, update):
        return await self._repo.update_one(self._collection, query, update)
    
    async def delete_one(self, query):
        return await self._repo.delete_one(self._collection, query)
    
    async def distinct(self, field: str):
        return await self._repo.distinct(self._collection, field)


_db_instance = None

async def get_database():
    """Dependency to get database connection"""
    global _db_instance
    if _db_instance is None:
        repo = get_repository()
        _db_instance = JSONDatabase(repo)
    return _db_instance

async def connect_to_mongo():
    """Initialize JSON file storage"""
    try:
        repo = get_repository()
        logger.info("✅ JSON file storage initialized")
        print("✅ JSON file storage initialized")
    except Exception as e:
        logger.error(f"❌ Error initializing storage: {e}")
        print(f"❌ Error initializing storage: {e}")

async def close_mongo_connection():
    """Cleanup JSON storage (if needed)"""
    logger.info("✅ JSON storage cleanup complete")
    print("✅ JSON storage cleanup complete")
