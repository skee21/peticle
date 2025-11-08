from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PetBase(BaseModel):
    name: str
    species: str
    breed: str
    age: Optional[int] = None
    weight: Optional[float] = None
    gender: str
    dob: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


class PetCreate(PetBase):
    """Schema for creating a pet"""
    pass


class PetUpdate(BaseModel):
    """Schema for updating a pet - all fields optional"""
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


class PetResponse(PetBase):
    """Schema for pet response"""
    id: str
    image: Optional[str] = None
    health_score: int
    videos_analyzed: int
    appointments: int
    medical_history: List[dict] = []
    created_at: str  # Changed to string for JSON compatibility
    updated_at: str  # Changed to string for JSON compatibility
    
    class Config:
        from_attributes = True
