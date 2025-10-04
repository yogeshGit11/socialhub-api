from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("SocialHub API", env="PROJECT_NAME")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(1, env="REFRESH_TOKEN_EXPIRE_DAYS")

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    MEDIA_DIR: str = Field("./app/static_media", env="MEDIA_DIR")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
