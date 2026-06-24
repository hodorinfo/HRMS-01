"""Employee Tags endpoints."""
from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import EmployeeTag
from app.schemas import EmployeeTagCreate, EmployeeTagRead, EmployeeTagUpdate

router = APIRouter()
router.include_router(create_crud_router("/tags", EmployeeTag, EmployeeTagCreate, EmployeeTagUpdate, EmployeeTagRead, get_db, get_current_user, "employees"))
