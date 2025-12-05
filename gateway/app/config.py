"""Configuration settings."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # Service info
    SERVICE_NAME: str = "SPARTA API Gateway"
    VERSION: str = "0.1.0"
    
    # URLs
    ORCHESTRATOR_URL: str = "http://localhost:8001"
    
    # Database
    DATABASE_URL: str = "postgresql://sparta:sparta_dev_password@localhost:5432/sparta"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60


settings = Settings()
