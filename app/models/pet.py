from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PetModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    species: str
    breed: str
    age: Optional[int] = None
    weight: Optional[float] = None
    gender: str
    dob: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    health_score: int = 90
    videos_analyzed: int = 0
    appointments: int = 0
    medical_history: List[dict] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
