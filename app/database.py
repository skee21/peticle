import json
import os
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)

# Directory to store JSON files
DB_DIR = Path(settings.database_dir)
DB_DIR.mkdir(exist_ok=True)

class JSONDatabase:
    """JSON-based database implementation"""
    
    def __init__(self, db_dir: str = "data"):
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(exist_ok=True)
        self._locks = {}  # Simple in-memory locks (for basic thread safety)
    
    def _get_collection_path(self, collection_name: str) -> Path:
        """Get the file path for a collection"""
        return self.db_dir / f"{collection_name}.json"
    
    def _load_collection(self, collection_name: str) -> List[Dict]:
        """Load a collection from JSON file"""
        file_path = self._get_collection_path(collection_name)
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Deserialize datetime fields
                if isinstance(data, list):
                    return [self._deserialize_document(doc) for doc in data]
                return []
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading collection {collection_name}: {e}")
            return []
    
    def _serialize_value(self, value):
        """Serialize a value for JSON storage"""
        if isinstance(value, datetime):
            return value.isoformat()
        return value
    
    def _serialize_document(self, doc: Dict) -> Dict:
        """Serialize a document for JSON storage"""
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, dict):
                serialized[key] = self._serialize_document(value)
            elif isinstance(value, list):
                serialized[key] = [self._serialize_value(item) if not isinstance(item, dict) else self._serialize_document(item) for item in value]
            else:
                serialized[key] = self._serialize_value(value)
        return serialized
    
    def _save_collection(self, collection_name: str, data: List[Dict]):
        """Save a collection to JSON file"""
        file_path = self._get_collection_path(collection_name)
        try:
            # Serialize all documents
            serialized_data = [self._serialize_document(doc) for doc in data]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(serialized_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving collection {collection_name}: {e}")
            raise
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())
    
    def find_one(self, collection_name: str, query: Dict) -> Optional[Dict]:
        """Find one document matching the query"""
        collection = self._load_collection(collection_name)
        
        for doc in collection:
            if self._match_query(doc, query):
                return doc.copy()
        return None
    
    def find(self, collection_name: str, query: Optional[Dict] = None) -> List[Dict]:
        """Find all documents matching the query"""
        collection = self._load_collection(collection_name)
        
        if query is None:
            return [doc.copy() for doc in collection]
        
        results = []
        for doc in collection:
            if self._match_query(doc, query):
                results.append(doc.copy())
        return results
    
    def _match_query(self, doc: Dict, query: Dict) -> bool:
        """Check if a document matches the query"""
        for key, value in query.items():
            if key not in doc:
                return False
            if doc[key] != value:
                return False
        return True
    
    def insert_one(self, collection_name: str, document: Dict) -> Dict:
        """Insert one document into collection"""
        collection = self._load_collection(collection_name)
        
        # Generate ID if not present
        if "_id" not in document and "id" not in document:
            document["_id"] = self._generate_id()
        elif "id" in document and "_id" not in document:
            document["_id"] = document["id"]
        
        # Ensure created_at if not present
        if "created_at" not in document:
            document["created_at"] = datetime.utcnow()
        
        # Ensure updated_at if not present (for pet model)
        if "updated_at" not in document:
            document["updated_at"] = datetime.utcnow()
        
        collection.append(document)
        self._save_collection(collection_name, collection)
        
        return {"inserted_id": document.get("_id")}
    
    def update_one(self, collection_name: str, query: Dict, update: Dict) -> Dict:
        """Update one document matching the query"""
        collection = self._load_collection(collection_name)
        
        matched_count = 0
        modified_count = 0
        
        for i, doc in enumerate(collection):
            if self._match_query(doc, query):
                matched_count = 1
                # Handle $set operations
                if "$set" in update:
                    for key, value in update["$set"].items():
                        doc[key] = value
                        modified_count = 1
                # Handle $inc operations
                elif "$inc" in update:
                    for key, value in update["$inc"].items():
                        if key in doc:
                            doc[key] = doc[key] + value
                        else:
                            doc[key] = value
                        modified_count = 1
                # Direct update (merge)
                else:
                    doc.update(update)
                    modified_count = 1
                
                # Update updated_at if field exists
                if "updated_at" in doc:
                    doc["updated_at"] = datetime.utcnow()
                
                break
        
        if modified_count > 0:
            self._save_collection(collection_name, collection)
        
        return {"matched_count": matched_count, "modified_count": modified_count}
    
    def delete_one(self, collection_name: str, query: Dict) -> Dict:
        """Delete one document matching the query"""
        collection = self._load_collection(collection_name)
        
        deleted_count = 0
        for i, doc in enumerate(collection):
            if self._match_query(doc, query):
                collection.pop(i)
                deleted_count = 1
                break
        
        if deleted_count > 0:
            self._save_collection(collection_name, collection)
        
        return {"deleted_count": deleted_count}
    
    def distinct(self, collection_name: str, field: str) -> List:
        """Get distinct values for a field"""
        collection = self._load_collection(collection_name)
        distinct_values = set()
        
        for doc in collection:
            if field in doc:
                distinct_values.add(doc[field])
        
        return list(distinct_values)
    
    def _deserialize_value(self, value):
        """Deserialize a value from JSON storage"""
        if isinstance(value, str):
            # Try to parse ISO datetime strings
            try:
                return datetime.fromisoformat(value)
            except (ValueError, AttributeError):
                return value
        return value

    def _deserialize_document(self, doc: Dict) -> Dict:
        """Deserialize a document from JSON storage"""
        deserialized = {}
        for key, value in doc.items():
            if key in ['created_at', 'updated_at', 'dob']:  # datetime fields
                deserialized[key] = self._deserialize_value(value)
            elif isinstance(value, dict):
                deserialized[key] = self._deserialize_document(value)
            elif isinstance(value, list):
                deserialized[key] = [
                    self._deserialize_value(item) if not isinstance(item, dict) 
                    else self._deserialize_document(item) for item in value
                ]
            else:
                deserialized[key] = value
        return deserialized


# Global database instance
db = JSONDatabase(db_dir=settings.database_dir)

async def get_database():
    """Dependency to get database connection"""
    return db

async def connect_to_mongo():
    """Initialize JSON database (kept for compatibility)"""
    logger.info("✅ JSON database initialized")
    print("✅ JSON database initialized")

async def close_mongo_connection():
    """Close JSON database (kept for compatibility)"""
    logger.info("❌ JSON database connection closed")
    print("❌ JSON database connection closed")
