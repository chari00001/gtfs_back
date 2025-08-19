from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    PROJECT_NAME: str = "GTFS Backend"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[str] = []

    MAPBOX_PUBLIC_TOKEN: str | None = None
    MAPBOX_SECRET_TOKEN: str | None = None

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/gtfs_db"



@lru_cache
def get_settings() -> Settings:
    return Settings()


