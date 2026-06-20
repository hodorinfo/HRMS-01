"""Celery worker for identity service."""
from horilla_common.celery_app import create_celery_app
from app.config import get_settings

settings = get_settings()
celery_app = create_celery_app("identity", settings.celery_broker_url, settings.celery_result_backend, ["app.tasks"])
