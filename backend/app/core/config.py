"""
Application configuration settings
Using pydantic-settings for environment variable management
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str = "sqlite:///./fashion_store.db"
    DB_PATH: str = "F:\\My_Repo\\Github\\20251119_Fashion-Store-MVP\\backend\\fashion_store.db"

    # App Settings
    APP_NAME: str = "Fashion Store MVP"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS Settings
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Image Settings
    IMAGE_BASE_PATH: str = "../fashion-dataset/images"

    # Ollama Settings (for AI features in Phase 3)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True,
    )

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]


# Create settings instance
settings = Settings()
