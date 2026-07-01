from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models import (
    Company, Department, JobPosition, JobRole, WorkType, EmployeeType, EmployeeShift,
    Holidays, WorkTypeRequest, MultipleApprovalCondition,
    EmployeeShiftDay, EmployeeShiftSchedule, RotatingWorkType,
    RotatingShift, RotatingShiftAssign, CompanyLeaves, MultipleApprovalManagers,
    Announcement, HorillaMailTemplate, AnnouncementComment, AnnouncementView
)
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyRead
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentRead
from app.schemas.jobposition import JobPositionCreate, JobPositionUpdate, JobPositionRead
from app.schemas.jobrole import JobRoleCreate, JobRoleUpdate, JobRoleRead
from app.schemas.worktype import WorkTypeCreate, WorkTypeUpdate, WorkTypeRead
from app.schemas.employeetype import EmployeeTypeCreate, EmployeeTypeUpdate, EmployeeTypeRead
from app.schemas.employeeshift import EmployeeShiftCreate, EmployeeShiftUpdate, EmployeeShiftRead
from app.schemas.holidays import HolidaysCreate, HolidaysUpdate, HolidaysRead
from app.schemas.worktyperequest import WorkTypeRequestCreate, WorkTypeRequestUpdate, WorkTypeRequestRead
from app.schemas.multipleapprovalcondition import MultipleApprovalConditionCreate, MultipleApprovalConditionUpdate, MultipleApprovalConditionRead
from app.schemas.employeeshiftday import EmployeeShiftDayCreate, EmployeeShiftDayUpdate, EmployeeShiftDayRead
from app.schemas.employeeshiftschedule import EmployeeShiftScheduleCreate, EmployeeShiftScheduleUpdate, EmployeeShiftScheduleRead
from app.schemas.rotatingworktype import RotatingWorkTypeCreate, RotatingWorkTypeUpdate, RotatingWorkTypeRead
from app.schemas.rotatingshift import RotatingShiftCreate, RotatingShiftUpdate, RotatingShiftRead
from app.schemas.rotatingshiftassign import RotatingShiftAssignCreate, RotatingShiftAssignUpdate, RotatingShiftAssignRead
from app.schemas.companyleaves import CompanyLeavesCreate, CompanyLeavesUpdate, CompanyLeavesRead
from app.schemas.multipleapprovalmanagers import MultipleApprovalManagersCreate, MultipleApprovalManagersUpdate, MultipleApprovalManagersRead
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementRead
from app.schemas.horillamailtemplate import HorillaMailTemplateCreate, HorillaMailTemplateUpdate, HorillaMailTemplateRead
from app.schemas.announcementcomment import AnnouncementCommentCreate, AnnouncementCommentUpdate, AnnouncementCommentRead
from app.schemas.announcementview import AnnouncementViewCreate, AnnouncementViewUpdate, AnnouncementViewRead

from app.routers import health, rotating_work_type_assigns, shift_request_comments, shift_requests

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(rotating_work_type_assigns.router)
api_router.include_router(shift_request_comments.router)
api_router.include_router(shift_requests.router)
for prefix, model, create, update, read in [
    ("/companies", Company, CompanyCreate, CompanyUpdate, CompanyRead),
    ("/departments", Department, DepartmentCreate, DepartmentUpdate, DepartmentRead),
    ("/job-positions", JobPosition, JobPositionCreate, JobPositionUpdate, JobPositionRead),
    ("/job-roles", JobRole, JobRoleCreate, JobRoleUpdate, JobRoleRead),
    ("/work-types", WorkType, WorkTypeCreate, WorkTypeUpdate, WorkTypeRead),
    ("/employee-types", EmployeeType, EmployeeTypeCreate, EmployeeTypeUpdate, EmployeeTypeRead),
    ("/shifts", EmployeeShift, EmployeeShiftCreate, EmployeeShiftUpdate, EmployeeShiftRead),
    ("/shift-days", EmployeeShiftDay, EmployeeShiftDayCreate, EmployeeShiftDayUpdate, EmployeeShiftDayRead),
    ("/shift-schedules", EmployeeShiftSchedule, EmployeeShiftScheduleCreate, EmployeeShiftScheduleUpdate, EmployeeShiftScheduleRead),
    ("/rotating-work-types", RotatingWorkType, RotatingWorkTypeCreate, RotatingWorkTypeUpdate, RotatingWorkTypeRead),
    ("/rotating-shifts", RotatingShift, RotatingShiftCreate, RotatingShiftUpdate, RotatingShiftRead),
    ("/rotating-shift-assigns", RotatingShiftAssign, RotatingShiftAssignCreate, RotatingShiftAssignUpdate, RotatingShiftAssignRead),
    ("/company-leaves", CompanyLeaves, CompanyLeavesCreate, CompanyLeavesUpdate, CompanyLeavesRead),
    ("/holidays", Holidays, HolidaysCreate, HolidaysUpdate, HolidaysRead),
    ("/work-type-requests", WorkTypeRequest, WorkTypeRequestCreate, WorkTypeRequestUpdate, WorkTypeRequestRead),
    ("/approval-conditions", MultipleApprovalCondition, MultipleApprovalConditionCreate, MultipleApprovalConditionUpdate, MultipleApprovalConditionRead),
    ("/approval-managers", MultipleApprovalManagers, MultipleApprovalManagersCreate, MultipleApprovalManagersUpdate, MultipleApprovalManagersRead),
    ("/announcements", Announcement, AnnouncementCreate, AnnouncementUpdate, AnnouncementRead),
    ("/announcement-comments", AnnouncementComment, AnnouncementCommentCreate, AnnouncementCommentUpdate, AnnouncementCommentRead),
    ("/announcement-views", AnnouncementView, AnnouncementViewCreate, AnnouncementViewUpdate, AnnouncementViewRead),
    ("/mail-templates", HorillaMailTemplate, HorillaMailTemplateCreate, HorillaMailTemplateUpdate, HorillaMailTemplateRead),
]:
    model_name = model.__name__.lower()
    api_router.include_router(create_crud_router(
        prefix, model, create, update, read, get_db, get_current_user, "base",
        get_permission_dep=lambda action, mn=model_name: require_permission(f"core.{action}_{mn}"),
    ))
