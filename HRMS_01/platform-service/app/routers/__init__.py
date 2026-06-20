from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import MailAutomation, Notification, DocumentRequest, Document
from app.schemas import (
    MailAutomationCreate, MailAutomationCreate, MailAutomationRead,
    NotificationCreate, NotificationCreate, NotificationRead,
    DocumentRequestCreate, DocumentRequestCreate, DocumentRequestRead,
    DocumentCreate, DocumentUpdate, DocumentRead,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read in [
    ("/automations", MailAutomation, MailAutomationCreate, MailAutomationCreate, MailAutomationRead),
    ("/notifications", Notification, NotificationCreate, NotificationCreate, NotificationRead),
    ("/document-requests", DocumentRequest, DocumentRequestCreate, DocumentRequestCreate, DocumentRequestRead),
    ("/documents", Document, DocumentCreate, DocumentUpdate, DocumentRead),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, "base"))
