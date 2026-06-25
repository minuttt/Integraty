from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Integraty"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "localhost"
    PORT: int = 8080

    # Database
    DATABASE_URL: str = "sqlite:///./data/database/integraty.db"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_SECRET: str = "dev-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Encryption
    ENCRYPTION_KEY: Optional[str] = None

    # Monitoring
    SCREENSHOT_INTERVAL: int = 30
    SCREENSHOT_QUALITY: int = 85
    MAX_SESSION_DURATION_HOURS: int = 8

    # Storage
    DATA_DIR: Path = Path("./data")
    SCREENSHOTS_DIR: Path = DATA_DIR / "screenshots"
    REPORTS_DIR: Path = DATA_DIR / "reports"
    DATABASE_DIR: Path = DATA_DIR / "database"
    LOGS_DIR: Path = DATA_DIR / "logs"

    # OCR
    OCR_ENABLED: bool = True
    TESSERACT_PATH: Optional[str] = None

    # Features
    ENABLE_BROWSER_MONITORING: bool = True
    ENABLE_WINDOW_MONITORING: bool = True
    ENABLE_OCR: bool = True

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
settings.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
