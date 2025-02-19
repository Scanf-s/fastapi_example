from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        extra="ignore",
        case_sensitive=True
    )

    DEV_MODE: bool = Field(default=False)
    DATABASE_URL: str = Field(default="sqlite:///database.db")
    BASE_API_URI: str = Field(default="/api/v1")
    JWT_SECRET: str = Field(default="secret1234")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
