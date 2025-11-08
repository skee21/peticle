from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    email: EmailStr
    full_name: str
    hashed_password: str
    phone: Optional[str] = None
    pets: List[str] = []  # List of pet IDs
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
