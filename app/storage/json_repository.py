import json
import os
import asyncio
import uuid
import copy
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path

class JSONRepository:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._locks = {}
        self._cache = {}
    
    def _get_lock(self, collection: str) -> asyncio.Lock:
        if collection not in self._locks:
            self._locks[collection] = asyncio.Lock()
        return self._locks[collection]
    
    def _get_file_path(self, collection: str) -> Path:
        return self.data_dir / f"{collection}.json"
    
    async def _load_data(self, collection: str) -> List[Dict]:
        file_path = self._get_file_path(collection)
        
        if collection in self._cache:
            return self._cache[collection]
        
        if not file_path.exists():
            self._cache[collection] = []
            return []
        
        try:
            async with asyncio.Lock():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self._cache[collection] = data
                    return data
        except Exception as e:
            print(f"Error loading {collection}: {e}")
            self._cache[collection] = []
            return []
    
    async def _save_data(self, collection: str, data: List[Dict]):
        file_path = self._get_file_path(collection)
        temp_path = file_path.with_suffix('.tmp')
        
        try:
            # Write to temp file first
            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            # Atomic rename
            temp_path.replace(file_path)
            self._cache[collection] = data
        except Exception as e:
            print(f"Error saving {collection}: {e}")
            if temp_path.exists():
                temp_path.unlink()
            raise
    
    async def insert_one(self, collection: str, document: Dict) -> Dict:
        async with self._get_lock(collection):
            data = await self._load_data(collection)
            
            # Generate ID if not present
            if "_id" not in document:
                document["_id"] = str(uuid.uuid4())
            
            # Add timestamps
            if "created_at" not in document:
                document["created_at"] = datetime.utcnow().isoformat()
            if "updated_at" not in document:
                document["updated_at"] = datetime.utcnow().isoformat()
            
            data.append(document)
            await self._save_data(collection, data)
            
            return {"inserted_id": document["_id"]}
    
    async def find(self, collection: str, query: Optional[Dict] = None) -> List[Dict]:
        async with self._get_lock(collection):
            data = await self._load_data(collection)
            
            if not query:
                return copy.deepcopy(data)
            
            # Simple query matching
            results = []
            for doc in data:
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                if match:
                    results.append(copy.deepcopy(doc))
            
            return results
    
    async def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        results = await self.find(collection, query)
        return results[0] if results else None
    
    async def update_one(self, collection: str, query: Dict, update: Dict) -> Dict:
        async with self._get_lock(collection):
            data = await self._load_data(collection)
            
            modified_count = 0
            matched_count = 0
            
            for i, doc in enumerate(data):
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                
                if match:
                    matched_count += 1
                    # Apply $set operator
                    if "$set" in update:
                        for key, value in update["$set"].items():
                            data[i][key] = value
                        data[i]["updated_at"] = datetime.utcnow().isoformat()
                        modified_count += 1
                    break
            
            if modified_count > 0:
                await self._save_data(collection, data)
            
            return {
                "matched_count": matched_count,
                "modified_count": modified_count
            }
    
    async def delete_one(self, collection: str, query: Dict) -> Dict:
        async with self._get_lock(collection):
            data = await self._load_data(collection)
            
            deleted_count = 0
            for i, doc in enumerate(data):
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                
                if match:
                    data.pop(i)
                    deleted_count += 1
                    break
            
            if deleted_count > 0:
                await self._save_data(collection, data)
            
            return {"deleted_count": deleted_count}

# Global repository instance
_repository = None

def get_repository() -> JSONRepository:
    global _repository
    if _repository is None:
        _repository = JSONRepository()
    return _repository
