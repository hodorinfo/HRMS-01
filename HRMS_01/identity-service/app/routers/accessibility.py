"""Accessibility endpoints."""
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import DefaultAccessibility
from app.schemas import DefaultAccessibilityCreate, DefaultAccessibilityRead, DefaultAccessibilityUpdate

from fastapi import APIRouter
router = APIRouter()
router.include_router(create_crud_router("/accessibility", DefaultAccessibility, DefaultAccessibilityCreate, DefaultAccessibilityUpdate, DefaultAccessibilityRead, get_db, get_current_user, "base"))
