"""Shared Celery configuration factory."""

from celery import Celery


def create_celery_app(
    service_name: str,
    broker_url: str,
    result_backend: str,
    include_modules: list[str] | None = None,
) -> Celery:
    app = Celery(service_name, broker=broker_url, backend=result_backend)
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_default_retry_delay=60,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
    )
    if include_modules:
        app.conf.include = include_modules
    return app


def task_retry_kwargs(max_retries: int = 3) -> dict:
    return {
        "autoretry_for": (Exception,),
        "retry_backoff": True,
        "retry_backoff_max": 600,
        "retry_jitter": True,
        "max_retries": max_retries,
    }
