from horilla_common.celery_app import task_retry_kwargs
from horilla_common.events import EVENT_DEPARTMENT_DELETED, publish_event
from app.celery_worker import celery_app

@celery_app.task(name="core.publish_department_deleted", **task_retry_kwargs())
def publish_department_deleted(department_id: int):
    publish_event(celery_app, EVENT_DEPARTMENT_DELETED, {"department_id": department_id})
