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
    
    async def _load_data(self, collection: str, use_cache: bool = True) -> List[Dict]:
        file_path = self._get_file_path(collection)
        
        # Check cache first (outside lock for performance)
        if use_cache and collection in self._cache:
            return copy.deepcopy(self._cache[collection])
        
        # Use collection-specific lock
        async with self._get_lock(collection):
            # Double-check cache after acquiring lock
            if use_cache and collection in self._cache:
                return copy.deepcopy(self._cache[collection])
            
            if not file_path.exists():
                self._cache[collection] = []
                return []
            
            try:
                # Use synchronous file I/O directly (FastAPI handles async context)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._cache[collection] = data
                return copy.deepcopy(data)
            except Exception as e:
                print(f"Error loading {collection}: {e}")
                import traceback
                traceback.print_exc()
                self._cache[collection] = []
                return []
    
    async def _save_data(self, collection: str, data: List[Dict]):
        file_path = self._get_file_path(collection)
        temp_path = file_path.with_suffix('.tmp')
        
        try:
            # Use synchronous file I/O directly (FastAPI handles async context)
            # Write to temp file first
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            
            # Atomic rename (replace existing file)
            if file_path.exists():
                file_path.unlink()
            temp_path.replace(file_path)
            
            # Update cache after successful write
            self._cache[collection] = copy.deepcopy(data)
        except Exception as e:
            print(f"Error saving {collection}: {e}")
            import traceback
            traceback.print_exc()
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except:
                    pass
            raise
    
    async def insert_one(self, collection: str, document: Dict) -> Dict:
        async with self._get_lock(collection):
            # Load fresh data (bypass cache when modifying)
            data = await self._load_data(collection, use_cache=False)
            
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
        # Load data (will use lock internally if needed)
        data = await self._load_data(collection)
        
        if not query:
            return copy.deepcopy(data)
        
        # Simple query matching
        results = []
        for doc in data:
            match = True
            for key, value in query.items():
                # Handle string ID comparison
                if key == "_id" and isinstance(value, str):
                    if doc.get(key) != value:
                        match = False
                        break
                elif key not in doc or doc[key] != value:
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
            # Load fresh data (bypass cache when modifying)
            data = await self._load_data(collection, use_cache=False)
            
            modified_count = 0
            matched_count = 0
            
            for i, doc in enumerate(data):
                match = True
                for key, value in query.items():
                    # Handle string ID comparison
                    if key == "_id" and isinstance(value, str):
                        if doc.get(key) != value:
                            match = False
                            break
                    elif key not in doc or doc[key] != value:
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
            # Load fresh data (bypass cache when modifying)
            data = await self._load_data(collection, use_cache=False)
            
            deleted_count = 0
            for i, doc in enumerate(data):
                match = True
                for key, value in query.items():
                    # Handle string ID comparison
                    if key == "_id" and isinstance(value, str):
                        if doc.get(key) != value:
                            match = False
                            break
                    elif key not in doc or doc[key] != value:
                        match = False
                        break
                
                if match:
                    data.pop(i)
                    deleted_count += 1
                    break
            
            if deleted_count > 0:
                await self._save_data(collection, data)
            
            return {"deleted_count": deleted_count}
    
    async def distinct(self, collection: str, field: str) -> List[Any]:
        """Get distinct values for a field"""
        data = await self._load_data(collection)
        distinct_values = set()
        for doc in data:
            if field in doc:
                distinct_values.add(doc[field])
        return sorted(list(distinct_values))

# Global repository instance
_repository = None

def get_repository() -> JSONRepository:
    global _repository
    if _repository is None:
        _repository = JSONRepository()
    return _repository
