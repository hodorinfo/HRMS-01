"""Bonus points endpoints."""
from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import BonusPoint
from app.schemas import BonusPointCreate, BonusPointRead, BonusPointUpdate

router = APIRouter()
router.include_router(create_crud_router("/bonus-points", BonusPoint, BonusPointCreate, BonusPointUpdate, BonusPointRead, get_db, get_current_user, "employees"))
