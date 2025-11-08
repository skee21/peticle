from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class VideoAnalysisResponse(BaseModel):
    id: str
    pet_id: str
    video_path: str
    analysis_status: str
    insights: List[Dict]
    recommendations: List[str]
    confidence_score: Optional[float]
    created_at: datetime

class VideoUploadResponse(BaseModel):
    video_id: str
    message: str
    status: str
