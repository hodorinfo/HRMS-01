from horilla_common.celery_app import task_retry_kwargs
from app.celery_worker import celery_app

@celery_app.task(**task_retry_kwargs())
def send_notification(recipient_id: int, verb: str, description: str = ""):
    return {"status": "sent", "recipient_id": recipient_id}

@celery_app.task(**task_retry_kwargs())
def run_automation(automation_id: int, record_id: int):
    return {"status": "executed", "automation_id": automation_id}
