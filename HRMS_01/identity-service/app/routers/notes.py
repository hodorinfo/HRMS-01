"""Employee Notes endpoints."""
from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import EmployeeNote
from app.schemas import EmployeeNoteCreate, EmployeeNoteRead, EmployeeNoteUpdate

router = APIRouter()
router.include_router(create_crud_router("/notes", EmployeeNote, EmployeeNoteCreate, EmployeeNoteUpdate, EmployeeNoteRead, get_db, get_current_user, "employees"))
