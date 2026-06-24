import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from horilla_common.celery_app import task_retry_kwargs
from horilla_common.events import EVENT_NOTIFICATION_CREATE, EVENT_EMAIL_SEND
from app.celery_worker import celery_app
from app.config import get_settings
from app.database import engine
from app.models import Notification

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@celery_app.task(name="horilla_common.events.dispatch_event", **task_retry_kwargs())
def dispatch_event(event_name: str, payload: dict):
    if event_name == EVENT_NOTIFICATION_CREATE:
        handle_create_notification.delay(payload)
    elif event_name == EVENT_EMAIL_SEND:
        handle_send_email.delay(payload)

@celery_app.task(**task_retry_kwargs())
def handle_create_notification(payload: dict):
    # This runs synchronously in celery, but we need to run async db calls
    async def _save():
        async with AsyncSessionLocal() as session:
            notif = Notification(
                recipient_id=payload["recipient_id"],
                verb=payload["verb"],
                description=payload.get("description"),
                public=payload.get("public", True),
                timestamp=datetime.now(timezone.utc)
            )
            session.add(notif)
            await session.commit()
    
    asyncio.run(_save())
    return {"status": "created"}

@celery_app.task(**task_retry_kwargs())
def handle_send_email(payload: dict):
    settings = get_settings()
    msg = EmailMessage()
    msg.set_content(payload["body"], subtype="html")
    msg["Subject"] = payload["subject"]
    msg["From"] = settings.smtp_user
    msg["To"] = payload["to_email"]

    try:
        if "dummy" not in settings.smtp_user:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
            print(f"Email sent successfully to {payload['to_email']}")
        else:
            print(f"MOCK EMAIL (No credentials): To: {payload['to_email']}, Subject: {payload['subject']}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e
    return {"status": "sent"}

