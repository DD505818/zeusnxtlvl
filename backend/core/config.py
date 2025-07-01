from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZEUS° NXTLVL"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "zeus"
    COINBASE_API_KEY: str = "changeme"
    COINBASE_SECRET: str = "changeme"
    GEMINI_API_KEY: str = "changeme"
    GROQ_API_KEY: str = "changeme"
    OPENAI_API_KEY: str = "changeme"
    VECTOR_DB_URL: str = "http://localhost:8001"
    CONFIDENCE_THRESHOLD: float = 0.95
    EXPECTED_RETURN_THRESHOLD: float = 0.01
    MAX_DAILY_DRAWDOWN_PERCENT: float = 5.0

    class Config:
        env_file = ".env"

settings = Settings()
