from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZEUS° NXTLVL"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000
    CONFIDENCE_THRESHOLD: float = 0.95
    EXPECTED_RETURN_THRESHOLD: float = 0.05
    MAX_DAILY_DRAWDOWN_PERCENT: float = 0.2

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    VECTOR_DB_URL: str = "http://localhost:8001"
    GEMINI_API_KEY: str = "dummy"
    GROQ_API_KEY: str = "dummy"
    OPENAI_API_KEY: str = "dummy"
    COINBASE_API_KEY: str = "dummy"
    COINBASE_SECRET: str = "dummy"

    class Config:
        env_file = ".env"

settings = Settings()
