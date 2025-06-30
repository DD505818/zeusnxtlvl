from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZEUS° NXTLVL"
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
