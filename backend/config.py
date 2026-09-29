from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    app_name: str = "Site-FastAPI"
    debug: bool = True
    version: str = "0.1.0"

    # Security
    secret_key: str = "change-me-to-random-string-32-chars-min"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "sqlite:///./site.db"

    # OAuth
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    telegram_bot_token: Optional[str] = None  # For Telegram Login Widget or Bot API

    # Frontend
    frontend_url: str = "http://localhost:3000"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()