"""Employee CRUD endpoints."""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
import bcrypt
from sqlalchemy import func, select

from horilla_common.crud import create_crud_router
from horilla_common.events import EVENT_EMPLOYEE_CREATED, publish_event
from horilla_common.schemas import PaginatedResponse
from app.celery_worker import celery_app
from app.database import get_db
from app.dependencies import CurrentUser, DbSession, get_current_user
from app.models import Employee, EmployeeBankDetails, EmployeeWorkInformation, User
from app.schemas import (
    EmployeeBankDetailsCreate, EmployeeBankDetailsRead, EmployeeBankDetailsUpdate,
    EmployeeCreate, EmployeeRead, EmployeeUpdate,
    EmployeeWorkInformationCreate, EmployeeWorkInformationRead, EmployeeWorkInformationUpdate,
)

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("", response_model=PaginatedResponse[EmployeeRead])
async def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    is_active: bool | None = None,
    db: DbSession = None,
    _user: CurrentUser = None,
):
    query = select(Employee)
    if is_active is not None:
        query = query.where(Employee.is_active == is_active)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(query.offset((page - 1) * page_size).limit(page_size))
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=[EmployeeRead.model_validate(i) for i in items], total=total or 0, page=page, page_size=page_size, pages=pages)

@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee(employee_id: int, db: DbSession, _user: CurrentUser):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeRead.model_validate(emp)

@router.post("", response_model=EmployeeRead, status_code=201)
async def create_employee(data: EmployeeCreate, background_tasks: BackgroundTasks, db: DbSession, user: CurrentUser):
    existing = await db.execute(select(Employee).where(Employee.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")
    emp_data = data.model_dump(exclude={"password"})
    employee = Employee(**emp_data)
    if data.password:
        hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        u = User(username=data.email, email=data.email, password_hash=hashed_pw, first_name=data.employee_first_name, last_name=data.employee_last_name)
        db.add(u)
        await db.flush()
        employee.employee_user_id = u.id
    db.add(employee)
    await db.flush()
    await db.refresh(employee)
    publish_event(celery_app, EVENT_EMPLOYEE_CREATED, {"employee_id": employee.id, "email": employee.email, "company_id": None})
    return EmployeeRead.model_validate(employee)

@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee(employee_id: int, data: EmployeeUpdate, db: DbSession, _user: CurrentUser):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(employee, k, v)
    await db.flush()
    await db.refresh(employee)
    return EmployeeRead.model_validate(employee)

@router.delete("/{employee_id}", status_code=204)
async def delete_employee(employee_id: int, db: DbSession, _user: CurrentUser):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.is_active = False

work_info_router = create_crud_router("/work-info", EmployeeWorkInformation, EmployeeWorkInformationCreate, EmployeeWorkInformationUpdate, EmployeeWorkInformationRead, get_db, get_current_user, "employee")
bank_router = create_crud_router("/bank-details", EmployeeBankDetails, EmployeeBankDetailsCreate, EmployeeBankDetailsUpdate, EmployeeBankDetailsRead, get_db, get_current_user, "employee")
router.include_router(work_info_router)
router.include_router(bank_router)
