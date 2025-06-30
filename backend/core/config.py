from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZEUS° NXTLVL"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000
    CONFIDENCE_THRESHOLD: float = 0.95
    EXPECTED_RETURN_THRESHOLD: float = 0.01
    MAX_DAILY_DRAWDOWN_PERCENT: float = 0.1

    class Config:
        env_file = ".env"

settings = Settings()
