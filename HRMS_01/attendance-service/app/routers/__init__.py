from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Attendance, LeaveType, LeaveRequest, BiometricDevices, GeoFencing, FaceDetection, EmployeeFaceDetection
from app.schemas import (
    AttendanceCreate, AttendanceUpdate, AttendanceRead,
    LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeRead,
    LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestRead,
    BiometricDeviceCreate, BiometricDeviceRead, GeoFencingCreate, GeoFencingRead,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read in [
    ("/attendance", Attendance, AttendanceCreate, AttendanceUpdate, AttendanceRead),
    ("/leave-types", LeaveType, LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeRead),
    ("/leave-requests", LeaveRequest, LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestRead),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, "attendance"))
api_router.include_router(create_crud_router("/biometric-devices", BiometricDevices, BiometricDeviceCreate, BiometricDeviceCreate, BiometricDeviceRead, get_db, get_current_user, "attendance"))
api_router.include_router(create_crud_router("/geofencing", GeoFencing, GeoFencingCreate, GeoFencingCreate, GeoFencingRead, get_db, get_current_user, "attendance"))
