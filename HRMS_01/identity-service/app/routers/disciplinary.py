"""Disciplinary actions endpoints."""
from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Actiontype, DisciplinaryAction
from app.schemas import (
    ActiontypeCreate, ActiontypeRead, ActiontypeUpdate,
    DisciplinaryActionCreate, DisciplinaryActionRead, DisciplinaryActionUpdate
)

router = APIRouter()
router.include_router(create_crud_router("/action-types", Actiontype, ActiontypeCreate, ActiontypeUpdate, ActiontypeRead, get_db, get_current_user, "employees"))
router.include_router(create_crud_router("/disciplinary-actions", DisciplinaryAction, DisciplinaryActionCreate, DisciplinaryActionUpdate, DisciplinaryActionRead, get_db, get_current_user, "employees"))
