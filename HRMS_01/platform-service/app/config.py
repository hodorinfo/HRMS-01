"""Service configuration."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "horilla-platform-service"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://horilla:horilla@postgres:5432/horilla_platform"
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    permission_service_url: str = "http://permission-service:8000"
    core_service_url: str = "http://core-service:8000"
    identity_service_url: str = "http://identity-service:8000"
    upload_base: str = "/media/documents"
    max_file_size_mb: int = 150
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "dummy@gmail.com"
    smtp_password: str = "dummy"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.database_url.endswith("/horilla"):
        settings.database_url = settings.database_url[:-8] + "/platform_db"
    return settings
