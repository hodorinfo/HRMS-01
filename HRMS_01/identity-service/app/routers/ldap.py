"""LDAP settings endpoints."""
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import LDAPSettings
from app.schemas import LDAPSettingsCreate, LDAPSettingsRead, LDAPSettingsUpdate

from fastapi import APIRouter
router = APIRouter()
router.include_router(create_crud_router("/ldap", LDAPSettings, LDAPSettingsCreate, LDAPSettingsUpdate, LDAPSettingsRead, get_db, get_current_user, "base"))
