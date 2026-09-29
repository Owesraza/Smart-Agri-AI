from pydantic_settings import BaseSettings
from functools import lru_cache


from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_SQLITE_PATH = BACKEND_DIR / "smartagri.db"


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SmartAgri AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_BASE_URL: str = "http://localhost:8000"

    # Database (SQL engine: SQLite default, configurable to PostgreSQL/MySQL via env)
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DEFAULT_SQLITE_PATH}"
    MONGODB_URL: str = ""
    DATABASE_NAME: str = "smartagri_db"

    @property
    def resolved_database_url(self) -> str:
        if "sqlite" in self.DATABASE_URL:
            # If path is relative or standard SQLite URL, lock to permanent backend/smartagri.db
            if "///." in self.DATABASE_URL or self.DATABASE_URL.endswith("smartagri.db"):
                return f"sqlite+aiosqlite:///{DEFAULT_SQLITE_PATH}"
        return self.DATABASE_URL

    # JWT Authentication (loaded from .env — NEVER hardcode secrets in source)
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 Days (43,200 Minutes)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 365      # 1 Year
    # Password Reset
    RESET_TOKEN_EXPIRE_MINUTES: int = 1440    # 24 Hours

    # Phase 3 – AI Engine (loaded from .env)
    GEMINI_API_KEY: str = ""

    # Phase 4 – Live APIs (loaded from .env — NEVER hardcode API keys in source)
    OPENWEATHER_API_KEY: str = ""
    AGMARKNET_API_KEY: str = ""
    AGMARKNET_BASE_URL: str = "https://api.agmarknet.gov.in/v1/"

    # Cache TTLs (in seconds)
    WEATHER_CACHE_TTL_SECONDS: int = 1800  # 30 minutes
    MARKET_CACHE_TTL_SECONDS: int = 3600   # 1 hour

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
