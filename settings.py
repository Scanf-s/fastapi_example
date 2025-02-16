from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        extra="ignore",
        case_sensitive=True
    )

    DEV_MODE: bool
    DATABASE_URL: PostgresDsn

fastapi_settings = Settings()
