from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        extra="ignore",
        case_sensitive=True
    )

    DEV_MODE: bool = Field()
    DATABASE_URL: str = Field()
    BASE_API_URI: str = Field()
