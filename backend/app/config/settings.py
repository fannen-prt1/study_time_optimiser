"""
Application settings and configuration
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Resolve .env path relative to this file → backend/.env
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # App Info
    APP_NAME: str = "Study Time Optimizer API"
    APP_VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./study_optimizer.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-min-32-chars"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-this-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_HOST: str = "localhost"
    BACKEND_PORT: int = 5000
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001"
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [i.strip() for i in self.CORS_ORIGINS.split(",") if i.strip()]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Email Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@studyoptimizer.com"
    EMAIL_ENABLED: bool = False
    
    # ML Configuration
    ML_MODELS_PATH: str = "ml-engine/saved_models"
    ML_MIN_SESSIONS_FOR_TRAINING: int = 50
    ML_RETRAIN_INTERVAL_DAYS: int = 7
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Feature Flags
    ENABLE_ANALYTICS: bool = True
    ENABLE_GAMIFICATION: bool = True
    ENABLE_POMODORO: bool = True
    
    class Config:
        env_file = str(_ENV_FILE)
        case_sensitive = True
        extra = "ignore"


# Create global settings instance
settings = Settings()


# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")
