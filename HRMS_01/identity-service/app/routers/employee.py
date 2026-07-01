"""Employee CRUD endpoints."""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
import bcrypt
from sqlalchemy import func, select

from horilla_common.crud import create_crud_router
from horilla_common.events import EVENT_EMPLOYEE_CREATED, publish_event
from horilla_common.schemas import PaginatedResponse
from app.celery_worker import celery_app
from app.database import get_db
from app.dependencies import CurrentUser, DbSession, get_current_user, require_permission
from sqlalchemy.orm import selectinload
from app.models import Employee, EmployeeBankDetails, EmployeeWorkInformation, User, EmployeeTag, DisciplinaryAction, DisciplinaryActionEmployee, BonusPoint
from app.schemas import (
    EmployeeBankDetailsCreate, EmployeeBankDetailsRead, EmployeeBankDetailsUpdate,
    EmployeeCreate, EmployeeListItemRead, EmployeeRead, EmployeeUpdate, EmployeeProfileRead,
    EmployeeWorkInformationCreate, EmployeeWorkInformationRead, EmployeeWorkInformationUpdate,
    SetEmployeePasswordRequest, DisciplinaryActionRead, BonusPointRead
)
from app.tasks import send_employee_invitation_email_task
from horilla_common.jwt import create_access_token
from app.config import get_settings
from app.routers.auth import hash_password

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("", response_model=PaginatedResponse[EmployeeListItemRead])
async def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    is_active: bool | None = None,
    db: DbSession = None,
    _user: CurrentUser = None,
    _perm = Depends(require_permission("identity.view_employee")),
):
    query = select(Employee).options(selectinload(Employee.work_info))
    if is_active is not None:
        query = query.where(Employee.is_active == is_active)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(query.offset((page - 1) * page_size).limit(page_size))
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=[EmployeeListItemRead.model_validate(i) for i in items], total=total or 0, page=page, page_size=page_size, pages=pages)

@router.get("/me", response_model=EmployeeProfileRead)
async def get_my_employee_profile(
    db: DbSession,
    user: CurrentUser,
    _perm = Depends(require_permission("identity.view_ownprofile")),
):
    # Determine the employee ID. 
    # If the user is an employee, user.employee should exist, but let's query the DB directly to be sure.
    # The JWT token already contains `employee_id` in some token generations, but we can query by employee_user_id
    result = await db.execute(
        select(Employee)
        .options(selectinload(Employee.work_info), selectinload(Employee.bank_details))
        .where(Employee.employee_user_id == user.user_id)
    )
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee profile not found for the current user.")
    return EmployeeProfileRead.model_validate(emp)

@router.get("/{employee_id}", response_model=EmployeeProfileRead)
async def get_employee(
    employee_id: int,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("identity.view_employee")),
):
    result = await db.execute(
        select(Employee)
        .options(selectinload(Employee.work_info), selectinload(Employee.bank_details))
        .where(Employee.id == employee_id)
    )
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeProfileRead.model_validate(emp)

from fastapi import Request

@router.post("", response_model=EmployeeRead, status_code=201)
async def create_employee(data: EmployeeCreate, background_tasks: BackgroundTasks, db: DbSession, request: Request):
    user_count = await db.scalar(select(func.count()).select_from(User))
    
    # 1. Conditional Authentication Logic
    if user_count > 0:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = auth_header.split(" ")[1]
        try:
            settings = get_settings()
            from horilla_common.jwt import decode_token
            token_payload = decode_token(token, settings.jwt_secret_key, settings.jwt_algorithm)
            if "identity.add_employee" not in token_payload.permissions and not token_payload.is_superuser:
                raise HTTPException(status_code=403, detail="Permission denied: identity.add_employee")
            user_result = await db.execute(select(User).where(User.id == token_payload.user_id))
            token_user = user_result.scalar_one_or_none()
            if not token_user or token_user.token_version != token_payload.token_version:
                raise HTTPException(status_code=401, detail="Token is no longer valid")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    # 2. Check for duplicate email
    existing = await db.execute(select(Employee).where(Employee.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    emp_data = data.model_dump(exclude={"password"})
    employee = Employee(**emp_data)

    # 3. Create User Profile
    password_to_use = data.password if data.password else str(data.phone).strip()
    hashed_pw = bcrypt.hashpw(password_to_use.encode(), bcrypt.gensalt()).decode()

    # Automatically grant superadmin rights if this is the very first user
    is_first_user = (user_count == 0)

    u = User(
        username=data.email,
        email=data.email,
        password_hash=hashed_pw,
        first_name=data.employee_first_name,
        last_name=data.employee_last_name,
        is_staff=is_first_user,
        is_superuser=is_first_user,
    )
    db.add(u)
    await db.flush()

    if is_first_user:
        recount = await db.scalar(select(func.count()).select_from(User))
        if recount > 1:
            u.is_superuser = False
            u.is_staff = False
            await db.flush()

    # 4. Create Employee Profile linked to User
    employee.employee_user_id = u.id
    db.add(employee)
    await db.flush()
    await db.refresh(employee)
    
    publish_event(celery_app, EVENT_EMPLOYEE_CREATED, {"employee_id": employee.id, "email": employee.email, "company_id": None})
    return EmployeeRead.model_validate(employee)

@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("identity.change_employee")),
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = data.model_dump(exclude_unset=True)
            
    for k, v in update_data.items():
        setattr(employee, k, v)
    await db.flush()
    await db.refresh(employee)
    return EmployeeRead.model_validate(employee)

@router.delete("/{employee_id}", status_code=204)
async def delete_employee(
    employee_id: int,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("identity.delete_employee")),
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.is_active = False

@router.post("/{employee_id}/set-password")
async def set_employee_password(
    employee_id: int,
    data: SetEmployeePasswordRequest,
    db: DbSession,
    user: CurrentUser,
    _perm = Depends(require_permission("identity.change_employee")),
):
        
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    user_result = await db.execute(select(User).where(User.id == employee.employee_user_id))
    emp_user = user_result.scalar_one_or_none()
    
    if not emp_user:
        # Create user if it doesn't exist
        hashed_pw = hash_password(data.new_password)
        emp_user = User(
            username=employee.email, 
            email=employee.email, 
            password_hash=hashed_pw, 
            first_name=employee.employee_first_name, 
            last_name=employee.employee_last_name
        )
        db.add(emp_user)
        await db.flush()
        employee.employee_user_id = emp_user.id
    else:
        emp_user.password_hash = hash_password(data.new_password)
        
    await db.flush()
    return {"message": "Password updated successfully"}

@router.get("/{employee_id}/work-info", response_model=EmployeeWorkInformationRead)
async def get_employee_work_info(
    employee_id: int,
    db: DbSession,
    _user: CurrentUser,
    _perm = Depends(require_permission("identity.view_employeeworkinformation")),
):
    result = await db.execute(
        select(EmployeeWorkInformation).where(EmployeeWorkInformation.employee_id == employee_id)
    )
    wi = result.scalar_one_or_none()
    if not wi:
        raise HTTPException(status_code=404, detail="Work information not found for this employee")
    return EmployeeWorkInformationRead.model_validate(wi)

@router.get("/{employee_id}/disciplinary-actions", response_model=list[DisciplinaryActionRead])
async def get_employee_disciplinary_actions(
    employee_id: int,
    db: DbSession,
    user: CurrentUser,
    _perm = Depends(require_permission("identity.view_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .join(DisciplinaryActionEmployee)
        .where(DisciplinaryActionEmployee.employee_id == employee_id)
    )
    actions = result.scalars().all()
    items = []
    for action in actions:
        emp_ids = [a.employee_id for a in action.employee_assignments]
        items.append(DisciplinaryActionRead(
            id=action.id,
            employee_ids=emp_ids,
            action_id=action.action_id,
            description=action.description,
            unit_in=action.unit_in,
            days=action.days,
            hours=action.hours,
            start_date=action.start_date,
            attachment=action.attachment,
            is_active=action.is_active,
            created_at=action.created_at,
        ))
    return items

@router.get("/{employee_id}/bonus-points", response_model=BonusPointRead)
async def get_employee_bonus_points(
    employee_id: int,
    db: DbSession,
    user: CurrentUser,
    _perm = Depends(require_permission("identity.view_bonuspoint")),
):
    result = await db.execute(select(BonusPoint).where(BonusPoint.employee_id == employee_id))
    points = result.scalar_one_or_none()
    if not points:
        raise HTTPException(status_code=404, detail="Bonus points not found for this employee")
    return BonusPointRead.model_validate(points)

@router.post("/{employee_id}/send-invitation")
async def send_invitation(
    employee_id: int,
    db: DbSession,
    user: CurrentUser,
    _perm = Depends(require_permission("identity.change_employee")),
):
        
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    if not employee.email:
        raise HTTPException(status_code=400, detail="Employee does not have an email address")
        
    settings = get_settings()
    token_data = {"sub": employee.email, "type": "reset_password"}
    # Token valid for 72 hours for invitation
    token = create_access_token(token_data, settings.jwt_secret_key, settings.jwt_algorithm, 60 * 72)
    
    send_employee_invitation_email_task.delay(employee.email, token)
    return {"message": "Invitation sent successfully"}

@router.post("/{employee_id}/toggle-status")
async def toggle_employee_status(
    employee_id: int,
    db: DbSession,
    user: CurrentUser,
    _perm = Depends(require_permission("identity.change_employee")),
):
        
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    employee.is_active = not employee.is_active
    
    # Also toggle user status if exists
    if employee.employee_user_id:
        user_result = await db.execute(select(User).where(User.id == employee.employee_user_id))
        emp_user = user_result.scalar_one_or_none()
        if emp_user:
            emp_user.is_active = employee.is_active
            
    await db.flush()
    return {"message": f"Employee {'activated' if employee.is_active else 'deactivated'} successfully"}

work_info_router = create_crud_router(
    "/work-info", EmployeeWorkInformation, EmployeeWorkInformationCreate,
    EmployeeWorkInformationUpdate, EmployeeWorkInformationRead, get_db,
    get_current_user, "employees",
    get_permission_dep=lambda action: require_permission(f"identity.{action}_employeeworkinformation"),
)
bank_router = create_crud_router(
    "/bank-details", EmployeeBankDetails, EmployeeBankDetailsCreate,
    EmployeeBankDetailsUpdate, EmployeeBankDetailsRead, get_db,
    get_current_user, "employees",
    get_permission_dep=lambda action: require_permission(f"identity.{action}_employeebankdetails"),
)
router.include_router(work_info_router)
router.include_router(bank_router)
