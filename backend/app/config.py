import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/instagram_analysis")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    apify_token: str = os.getenv("APIFY_TOKEN", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key")
    
    class Config:
        env_file = ".env"

settings = Settings()