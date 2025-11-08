from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId

class VideoAnalysis(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    pet_id: str
    video_path: str
    thumbnail_path: Optional[str] = None
    duration: Optional[float] = None
    file_size: int
    analysis_status: str = "pending"  # pending, processing, completed, failed
    insights: List[Dict] = []
    recommendations: List[str] = []
    confidence_score: Optional[float] = None
    detected_behaviors: List[str] = []
    health_concerns: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    analyzed_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
