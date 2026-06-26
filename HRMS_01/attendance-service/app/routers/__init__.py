from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user

from app.models import (
    Attendance, LeaveType, LeaveRequest, BiometricDevices, GeoFencing, FaceDetection, EmployeeFaceDetection,
    AttendanceActivity, BatchAttendance, AttendanceOverTime, AttendanceLateComeEarlyOut, GraceTime, AttendanceGeneralSetting, WorkRecords,
    AvailableLeave, LeaveAllocationRequest, RestrictLeave, CompensatoryLeaveRequest, BiometricEmployees
)

from app.schemas import (
    AttendanceCreate, AttendanceUpdate, AttendanceRead,
    LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeRead,
    LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestRead,
    BiometricDeviceCreate, BiometricDeviceRead, GeoFencingCreate, GeoFencingRead,
    AttendanceActivityCreate, AttendanceActivityRead,
    BatchAttendanceCreate, BatchAttendanceRead,
    AttendanceOverTimeCreate, AttendanceOverTimeRead,
    AttendanceLateComeEarlyOutCreate, AttendanceLateComeEarlyOutRead,
    GraceTimeCreate, GraceTimeRead,
    AttendanceGeneralSettingCreate, AttendanceGeneralSettingRead,
    WorkRecordsCreate, WorkRecordsRead,
    AvailableLeaveCreate, AvailableLeaveRead,
    LeaveAllocationRequestCreate, LeaveAllocationRequestRead,
    RestrictLeaveCreate, RestrictLeaveRead,
    CompensatoryLeaveRequestCreate, CompensatoryLeaveRequestRead,
    BiometricEmployeesCreate, BiometricEmployeesRead,
    FaceDetectionCreate, FaceDetectionRead,
    EmployeeFaceDetectionCreate, EmployeeFaceDetectionRead
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)

for prefix, model, create, update, read, module_name in [
    # Attendance Core
    ("/attendance", Attendance, AttendanceCreate, AttendanceUpdate, AttendanceRead, "Attendance Core"),
    ("/attendance-activities", AttendanceActivity, AttendanceActivityCreate, AttendanceActivityCreate, AttendanceActivityRead, "Attendance Core"),
    ("/batch-attendance", BatchAttendance, BatchAttendanceCreate, BatchAttendanceCreate, BatchAttendanceRead, "Attendance Core"),
    ("/attendance-overtime", AttendanceOverTime, AttendanceOverTimeCreate, AttendanceOverTimeCreate, AttendanceOverTimeRead, "Attendance Core"),
    ("/attendance-late-early", AttendanceLateComeEarlyOut, AttendanceLateComeEarlyOutCreate, AttendanceLateComeEarlyOutCreate, AttendanceLateComeEarlyOutRead, "Attendance Core"),
    ("/grace-time", GraceTime, GraceTimeCreate, GraceTimeCreate, GraceTimeRead, "Attendance Settings"),
    ("/attendance-settings", AttendanceGeneralSetting, AttendanceGeneralSettingCreate, AttendanceGeneralSettingCreate, AttendanceGeneralSettingRead, "Attendance Settings"),
    ("/work-records", WorkRecords, WorkRecordsCreate, WorkRecordsCreate, WorkRecordsRead, "Attendance Core"),
    
    # Leave Management
    ("/leave-types", LeaveType, LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeRead, "Leave Management"),
    ("/leave-requests", LeaveRequest, LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestRead, "Leave Management"),
    ("/available-leave", AvailableLeave, AvailableLeaveCreate, AvailableLeaveCreate, AvailableLeaveRead, "Leave Management"),
    ("/leave-allocations", LeaveAllocationRequest, LeaveAllocationRequestCreate, LeaveAllocationRequestCreate, LeaveAllocationRequestRead, "Leave Management"),
    ("/restrict-leave", RestrictLeave, RestrictLeaveCreate, RestrictLeaveCreate, RestrictLeaveRead, "Leave Management"),
    ("/compensatory-leave", CompensatoryLeaveRequest, CompensatoryLeaveRequestCreate, CompensatoryLeaveRequestCreate, CompensatoryLeaveRequestRead, "Leave Management"),
    
    # Biometrics & Hardware
    ("/biometric-devices", BiometricDevices, BiometricDeviceCreate, BiometricDeviceCreate, BiometricDeviceRead, "Biometrics"),
    ("/biometric-employees", BiometricEmployees, BiometricEmployeesCreate, BiometricEmployeesCreate, BiometricEmployeesRead, "Biometrics"),
    
    # Face Detection
    ("/face-detection", FaceDetection, FaceDetectionCreate, FaceDetectionCreate, FaceDetectionRead, "Face Detection"),
    ("/employee-face-detection", EmployeeFaceDetection, EmployeeFaceDetectionCreate, EmployeeFaceDetectionCreate, EmployeeFaceDetectionRead, "Face Detection"),
    
    # Geofencing
    ("/geofencing", GeoFencing, GeoFencingCreate, GeoFencingCreate, GeoFencingRead, "Geofencing"),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, module_name))

# Register Legacy Actions (Custom Endpoints)
from app.routers import legacy_actions
api_router.include_router(legacy_actions.router)

# Register Status Endpoints
from app.routers import attendance_status
api_router.include_router(attendance_status.router, prefix="/attendance-status")
