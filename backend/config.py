from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Site-FastAPI"
    DEBUG: bool = True
    VERSION: str = "0.1.0"
    
    # Security
    SECRET_KEY: str = "change-me-to-random-string-32-chars-min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./site.db"
    
    # OAuth
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None  # For Telegram Login Widget or Bot API
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Admin API bearer token (temporary until full OAuth admin flow)
    ADMIN_TOKEN: Optional[str] = None
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()