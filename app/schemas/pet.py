from pydantic import BaseModel
from typing import Optional

class PetCreate(BaseModel):
    name: str
    species: str
    breed: str
    age: Optional[int] = None
    weight: Optional[float] = None
    gender: str
    dob: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    description: Optional[str] = None

class PetResponse(BaseModel):
    id: str
    name: str
    species: str
    breed: str
    age: Optional[int]
    weight: Optional[float]
    gender: str
    health_score: int
    image: Optional[str]
    
    class Config:
        from_attributes = True
