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
