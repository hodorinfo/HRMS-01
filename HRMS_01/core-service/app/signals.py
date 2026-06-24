from sqlalchemy import event
from app.models import Announcement, WorkTypeRequest, ShiftRequest
from horilla_common.events import notify
from app.celery_worker import celery_app

def after_insert_announcement(mapper, connection, target):
    """Triggered when a new Announcement is created."""
    # We send a notification to a generic 'all' or broadcast it.
    # For now we use recipient_id=0 as a broadcast signal.
    notify(
        celery_app=celery_app,
        recipient_id=0,  # 0 indicates broadcast to all active employees
        verb=f"New Announcement: {target.title}",
        description=target.description,
        public=True
    )

def after_insert_worktyperequest(mapper, connection, target):
    """Triggered when a new WorkTypeRequest is created."""
    notify(
        celery_app=celery_app,
        recipient_id=target.employee_id, # Actually this should notify the MANAGER, but since we don't have manager ID in the hook easily, we notify the employee for now, or route to a specific task.
        verb="Work Type Request Submitted",
        description=target.description,
        public=False
    )

def after_insert_shiftrequest(mapper, connection, target):
    """Triggered when a new ShiftRequest is created."""
    notify(
        celery_app=celery_app,
        recipient_id=target.employee_id,
        verb="Shift Request Submitted",
        description=target.description,
        public=False
    )

def register_signals():
    event.listen(Announcement, 'after_insert', after_insert_announcement)
    event.listen(WorkTypeRequest, 'after_insert', after_insert_worktyperequest)
    event.listen(ShiftRequest, 'after_insert', after_insert_shiftrequest)
