from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZEUS° NXTLVL"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "zeus"

    VECTOR_DB_URL: str = "http://localhost:8080"

    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    COINBASE_API_KEY: str = ""
    COINBASE_SECRET: str = ""

    CONFIDENCE_THRESHOLD: float = 0.95
    EXPECTED_RETURN_THRESHOLD: float = 0.05
    MAX_DAILY_DRAWDOWN_PERCENT: float = 0.1

    class Config:
        env_file = Path(__file__).resolve().parents[2] / '.env'

settings = Settings()
