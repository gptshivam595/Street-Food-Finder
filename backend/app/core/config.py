from __future__ import annotations

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_URL: str = "http://localhost:3000"
    SECRET_KEY: str = "changeme"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    ALLOWED_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    @model_validator(mode="after")
    def populate_allowed_origins(self) -> "Settings":
        origins = {
            "http://localhost:3000",
            "http://localhost:3001",
            self.FRONTEND_URL,
        }
        if self.ENVIRONMENT == "development":
            origins.add("http://127.0.0.1:3000")
        self.ALLOWED_ORIGINS = sorted(origin for origin in origins if origin)
        return self


settings = Settings()
