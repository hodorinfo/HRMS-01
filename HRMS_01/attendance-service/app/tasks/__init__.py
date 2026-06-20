from horilla_common.celery_app import task_retry_kwargs
from horilla_common.events import EVENT_EMPLOYEE_CREATED
from app.celery_worker import celery_app

@celery_app.task(name="horilla_common.events.dispatch_event", **task_retry_kwargs())
def dispatch_event(event_name: str, payload: dict):
    if event_name == EVENT_EMPLOYEE_CREATED:
        setup_employee_attendance.delay(payload)

@celery_app.task(**task_retry_kwargs())
def setup_employee_attendance(payload: dict):
    employee_id = payload.get("employee_id")
    return {"status": "attendance_config_created", "employee_id": employee_id}
