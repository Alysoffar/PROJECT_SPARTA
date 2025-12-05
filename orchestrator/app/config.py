"""Configuration settings for orchestrator."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Orchestrator settings."""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # Service info
    SERVICE_NAME: str = "SPARTA Orchestrator"
    VERSION: str = "0.1.0"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://sparta:sparta_dev_password@localhost:5672/"
    
    # Agent URLs
    NLP_AGENT_URL: str = "http://localhost:8010"
    SYNTHESIS_AGENT_URL: str = "http://localhost:8011"
    OPTIMIZATION_AGENT_URL: str = "http://localhost:8012"
    VISUALIZATION_AGENT_URL: str = "http://localhost:8013"
    
    # Service URLs
    EMULATOR_URL: str = "http://localhost:8020"
    RTL_GENERATOR_URL: str = "http://localhost:8021"
    MODEL_SYNTHESIS_URL: str = "http://localhost:8022"
    COMPILER_URL: str = "http://localhost:8023"


settings = Settings()
