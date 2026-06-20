"""Outlook OAuth endpoints."""
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import AzureApi
from app.schemas import AzureApiCreate, AzureApiRead, AzureApiUpdate

from fastapi import APIRouter
router = APIRouter()
router.include_router(create_crud_router("/outlook", AzureApi, AzureApiCreate, AzureApiUpdate, AzureApiRead, get_db, get_current_user, "base"))
