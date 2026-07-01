"""Celery worker for project-service (stub — can be extended for async tasks)."""

from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "project_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.task_routes = {}
