from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models import MailAutomation, Notification
from app.schemas import (
    MailAutomationCreate, MailAutomationCreate, MailAutomationRead,
    NotificationCreate, NotificationCreate, NotificationRead,
)
from app.routers import documents, document_requests, health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read in [
    ("/automations", MailAutomation, MailAutomationCreate, MailAutomationCreate, MailAutomationRead),
    ("/notifications", Notification, NotificationCreate, NotificationCreate, NotificationRead),
]:
    model_name = model.__name__.lower()
    api_router.include_router(create_crud_router(
        prefix, model, create, update, read, get_db, get_current_user, "base",
        get_permission_dep=lambda action, mn=model_name: require_permission(f"platform.{action}_{mn}"),
    ))

api_router.include_router(document_requests.router)
api_router.include_router(documents.router)
