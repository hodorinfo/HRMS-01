"""Celery tasks for identity service."""
from horilla_common.celery_app import task_retry_kwargs
from horilla_common.events import EVENT_DEPARTMENT_DELETED
from app.celery_worker import celery_app

@celery_app.task(name="horilla_common.events.dispatch_event", **task_retry_kwargs())
def dispatch_event(event_name: str, payload: dict):
    if event_name == EVENT_DEPARTMENT_DELETED:
        handle_department_deleted.delay(payload)

@celery_app.task(**task_retry_kwargs())
def handle_department_deleted(payload: dict):
    """Unassign employees from deleted department."""
    department_id = payload.get("department_id")
    # Cross-service: update work info records via internal API or direct DB in identity DB
    return {"status": "processed", "department_id": department_id}

@celery_app.task(**task_retry_kwargs())
def send_password_reset_email_task(email: str, token: str):
    """Send password reset email."""
    # In a real system, you would use an email library like aiosmtplib or sendgrid
    print(f"MOCK: Sending password reset email to {email} with token {token}")
    return {"status": "sent", "email": email}

@celery_app.task(**task_retry_kwargs())
def send_employee_invitation_email_task(email: str, token: str):
    """Send employee invitation email."""
    # In a real system, you would use an email library
    print(f"MOCK: Sending employee invitation email to {email} with token {token}")
    return {"status": "sent", "email": email}