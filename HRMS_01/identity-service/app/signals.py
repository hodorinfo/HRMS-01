from sqlalchemy import event
from app.models import Employee
from horilla_common.events import send_email_event
from app.celery_worker import celery_app

def after_insert_employee(mapper, connection, target):
    """Triggered when a new Employee is created."""
    body = f"""
    <h2>Welcome to Horilla HRMS, {target.employee_first_name}!</h2>
    <p>We are excited to have you on board.</p>
    <p>Your Badge ID is: {target.badge_id if target.badge_id else 'Pending'}</p>
    <br>
    <p>Regards,<br>The HR Team</p>
    """
    
    send_email_event(
        celery_app=celery_app,
        to_email=target.email,
        subject="Welcome to Horilla HRMS!",
        body=body
    )

def register_signals():
    event.listen(Employee, 'after_insert', after_insert_employee)
