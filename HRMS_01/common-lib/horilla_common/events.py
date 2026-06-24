"""Celery event publishing helpers."""

from celery import Celery


def publish_event(
    celery_app: Celery,
    event_name: str,
    payload: dict,
    queue: str = "events",
) -> None:
    celery_app.send_task(
        "horilla_common.events.dispatch_event",
        args=[event_name, payload],
        queue=queue,
    )


EVENT_EMPLOYEE_CREATED = "employee.created"
EVENT_DEPARTMENT_DELETED = "department.deleted"
EVENT_EMPLOYEE_UPDATED = "employee.updated"
EVENT_LEAVE_APPROVED = "leave.approved"
EVENT_PAYSLIP_GENERATED = "payslip.generated"
EVENT_NOTIFICATION_CREATE = "notification.create"
EVENT_EMAIL_SEND = "email.send"

def notify(
    celery_app: Celery,
    recipient_id: int,
    verb: str,
    description: str = None,
    public: bool = True
) -> None:
    """Helper to publish a notification event."""
    payload = {
        "recipient_id": recipient_id,
        "verb": verb,
        "description": description,
        "public": public
    }
    publish_event(celery_app, EVENT_NOTIFICATION_CREATE, payload)

def send_email_event(
    celery_app: Celery,
    to_email: str,
    subject: str,
    body: str
) -> None:
    """Helper to publish an email sending event."""
    payload = {
        "to_email": to_email,
        "subject": subject,
        "body": body
    }
    publish_event(celery_app, EVENT_EMAIL_SEND, payload)
