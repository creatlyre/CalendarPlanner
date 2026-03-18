from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    GOOGLE_SCOPES: List[str] = Field(
        default_factory=lambda: [
            "openid",
            "profile",
            "email",
            "https://www.googleapis.com/auth/calendar",
        ]
    )

    # Supabase PostgreSQL connection string
    DATABASE_URL: str = "postgresql://user:password@host:5432/calendar"

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 8
    DB_ENCRYPTION_KEY: str = "your-encryption-key-for-oauth-tokens"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
