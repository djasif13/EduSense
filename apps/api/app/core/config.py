from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://edusense:edusense_dev@localhost:5432/edusense"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "change-me-in-production"
    
    class Config:
        env_file = ".env"

settings = Settings()
