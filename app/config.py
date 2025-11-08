from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    mongodb_url: str = Field(default="mongodb://localhost:27017", description="MongoDB connection URL")
    database_name: str = Field(default="petcare", description="Database name")
    secret_key: str = Field(default="dev-secret-key-change-in-production", description="Secret key for JWT tokens")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openai_api_key: Optional[str] = None
    google_maps_api_key: Optional[str] = None
    max_file_size: int = 104857600
    allowed_video_types: str = "video/mp4,video/avi,video/mov"
    allowed_image_types: str = "image/jpeg,image/png,image/jpg"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
