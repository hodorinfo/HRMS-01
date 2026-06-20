from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Company, Department, JobPosition, JobRole, WorkType, EmployeeType, EmployeeShift, Holidays, WorkTypeRequest, ShiftRequest, MultipleApprovalCondition
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyRead
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentRead
from app.schemas.jobposition import JobPositionCreate, JobPositionUpdate, JobPositionRead
from app.schemas.jobrole import JobRoleCreate, JobRoleUpdate, JobRoleRead
from app.schemas.worktype import WorkTypeCreate, WorkTypeUpdate, WorkTypeRead
from app.schemas.employeetype import EmployeeTypeCreate, EmployeeTypeUpdate, EmployeeTypeRead
from app.schemas.employeeshift import EmployeeShiftCreate, EmployeeShiftUpdate, EmployeeShiftRead
from app.schemas.holidays import HolidaysCreate, HolidaysUpdate, HolidaysRead
from app.schemas.worktyperequest import WorkTypeRequestCreate, WorkTypeRequestUpdate, WorkTypeRequestRead
from app.schemas.shiftrequest import ShiftRequestCreate, ShiftRequestUpdate, ShiftRequestRead
from app.schemas.multipleapprovalcondition import MultipleApprovalConditionCreate, MultipleApprovalConditionUpdate, MultipleApprovalConditionRead
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read in [
    ("/companies", Company, CompanyCreate, CompanyUpdate, CompanyRead),
    ("/departments", Department, DepartmentCreate, DepartmentUpdate, DepartmentRead),
    ("/job-positions", JobPosition, JobPositionCreate, JobPositionUpdate, JobPositionRead),
    ("/job-roles", JobRole, JobRoleCreate, JobRoleUpdate, JobRoleRead),
    ("/work-types", WorkType, WorkTypeCreate, WorkTypeUpdate, WorkTypeRead),
    ("/employee-types", EmployeeType, EmployeeTypeCreate, EmployeeTypeUpdate, EmployeeTypeRead),
    ("/shifts", EmployeeShift, EmployeeShiftCreate, EmployeeShiftUpdate, EmployeeShiftRead),
    ("/holidays", Holidays, HolidaysCreate, HolidaysUpdate, HolidaysRead),
    ("/work-type-requests", WorkTypeRequest, WorkTypeRequestCreate, WorkTypeRequestUpdate, WorkTypeRequestRead),
    ("/shift-requests", ShiftRequest, ShiftRequestCreate, ShiftRequestUpdate, ShiftRequestRead),
    ("/approval-conditions", MultipleApprovalCondition, MultipleApprovalConditionCreate, MultipleApprovalConditionUpdate, MultipleApprovalConditionRead),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, "base"))
