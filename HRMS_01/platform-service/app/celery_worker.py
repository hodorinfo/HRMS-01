from celery import Celery

from app.config import get_settings
settings = get_settings()

celery_app = Celery(
    "platform",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks"],
)

celery_app.conf.update(
    result_backend_always_retry=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


# expose for convenience in other services if needed
__all__ = ["celery_app"]
