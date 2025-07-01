from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZEUS° NXTLVL"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000

    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # PostgreSQL configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "zeus"

    # Vector database
    VECTOR_DB_URL: str = "http://localhost:6333"

    # API keys / brokers
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    COINBASE_API_KEY: str = ""
    COINBASE_SECRET: str = ""

    # Trading thresholds
    CONFIDENCE_THRESHOLD: float = 0.95
    EXPECTED_RETURN_THRESHOLD: float = 0.05
    MAX_DAILY_DRAWDOWN_PERCENT: float = 0.1

    class Config:
        env_file = ".env"

settings = Settings()
