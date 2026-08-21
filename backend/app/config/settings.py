"""
Application Settings using Pydantic BaseSettings.
"""
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FasalDisha-Backend"
    APP_ENV: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # CORS origins
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Database URL: defaults to local SQLite for instant zero-dependency fallback
    DATABASE_URL: str = "sqlite:///./fasal_disha.db"

    # Decision Engine Parameters
    RADIUS_KM_DEFAULT: float = 100.0
    RADIUS_KM_MAX: float = 300.0
    TRANSPORT_RATE_PER_QUINTAL_PER_KM: float = 2.5
    PEAK_ALERT_THRESHOLD: float = 0.05
    SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
