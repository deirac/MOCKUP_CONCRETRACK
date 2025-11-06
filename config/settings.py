import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    PROJECT_NAME: str = "ConcreTrack"
    VERSION: str = "1.0.7"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    
    # Server Config
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Paths
    STATIC_DIR: str = "static"
    TEMPLATES_DIR: str = "templates"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()