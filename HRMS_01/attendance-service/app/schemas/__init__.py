from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AttendanceCreate(BaseModel):
    employee_id: int
    attendance_date: date
    shift_id: Optional[int] = None
    work_type_id: Optional[int] = None
    attendance_clock_in_date: Optional[date] = None
    attendance_clock_in: Optional[str] = None
    attendance_clock_out_date: Optional[date] = None
    attendance_clock_out: Optional[str] = None
    attendance_worked_hour: Optional[str] = "00:00"
    minimum_hour: str = "00:00"
    is_validate_request: bool = True
    attendance_validated: bool = False
    request_description: Optional[str] = None
    request_type: Optional[str] = "create_request"
    is_holiday: bool = False

    @field_validator("attendance_date")
    @classmethod
    def validate_attendance_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Attendance date cannot be in the past")
        return v

class AttendanceUpdate(BaseModel):
    employee_id: Optional[int] = None
    attendance_date: Optional[date] = None
    shift_id: Optional[int] = None
    work_type_id: Optional[int] = None
    attendance_clock_in_date: Optional[date] = None
    attendance_clock_in: Optional[str] = None
    attendance_clock_out_date: Optional[date] = None
    attendance_clock_out: Optional[str] = None
    minimum_hour: Optional[str] = None
    attendance_validated: Optional[bool] = None
    attendance_overtime_approve: Optional[bool] = None
    request_description: Optional[str] = None
    is_holiday: Optional[bool] = None

class AttendanceRead(HorillaSchema):
    id: int
    employee_id: int
    attendance_date: date
    shift_id: Optional[int] = None
    work_type_id: Optional[int] = None
    attendance_clock_in_date: Optional[date] = None
    attendance_clock_in: Optional[str] = None
    attendance_clock_out_date: Optional[date] = None
    attendance_clock_out: Optional[str] = None
    attendance_worked_hour: Optional[str] = None
    minimum_hour: Optional[str] = None
    request_description: Optional[str] = None
    request_type: Optional[str] = None
    is_validate_request: bool = False
    attendance_validated: bool = False
    is_holiday: bool = False
    is_active: bool = True

class LeaveTypeCreate(BaseModel):
    name: str
    color: Optional[str] = None
    payment: str = "paid"
    count: float = 0
    period_in: str = "day"
    company_id: Optional[int] = None

class LeaveTypeUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    count: Optional[float] = None

class LeaveTypeRead(HorillaSchema):
    id: int
    name: str
    color: Optional[str] = None
    payment: str
    count: float
    is_active: bool = True

class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    requested_days: float
    description: Optional[str] = None
    start_date_breakdown: str = "full_day"
    end_date_breakdown: str = "full_day"

class LeaveRequestUpdate(BaseModel):
    status: Optional[str] = None
    reject_reason: Optional[str] = None

class LeaveRequestRead(HorillaSchema):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    requested_days: float
    status: str
    description: Optional[str] = None
    is_active: bool = True

class BiometricDeviceCreate(BaseModel):
    name: str
    machine_type: str
    machine_ip: Optional[str] = None
    port: Optional[int] = None
    company_id: Optional[int] = None

class BiometricDeviceRead(HorillaSchema):
    id: str
    name: str
    machine_type: str
    is_live: bool = False
    is_active: bool = True

class GeoFencingCreate(BaseModel):
    latitude: float
    longitude: float
    radius_in_meters: int
    company_id: Optional[int] = None
    start: bool = False

class GeoFencingRead(HorillaSchema):
    id: int
    latitude: float
    longitude: float
    radius_in_meters: int
    start: bool = False

# --- MISSING ATTENDANCE MODELS ---
class AttendanceActivityCreate(BaseModel):
    employee_id: int
    attendance_date: Optional[date] = None
    shift_day_id: Optional[int] = None
    in_datetime: Optional[str] = None
    out_datetime: Optional[str] = None
    clock_in_date: Optional[date] = None
    clock_out_date: Optional[date] = None
    clock_in: str
    clock_out: Optional[str] = None

class AttendanceActivityRead(HorillaSchema):
    id: int
    employee_id: int
    attendance_date: Optional[date] = None
    clock_in: str
    clock_out: Optional[str] = None
    is_active: bool = True

class BatchAttendanceCreate(BaseModel):
    title: str

class BatchAttendanceRead(HorillaSchema):
    id: int
    title: str
    is_active: bool = True

class AttendanceOverTimeCreate(BaseModel):
    employee_id: int
    month: str
    month_sequence: int
    year: str
    worked_hours: str
    pending_hours: str
    overtime: str
    hour_account_second: int
    hour_pending_second: int
    overtime_second: int

class AttendanceOverTimeRead(HorillaSchema):
    id: int
    employee_id: int
    month: str
    year: str
    overtime: str
    is_active: bool = True

class AttendanceLateComeEarlyOutCreate(BaseModel):
    attendance_id: int
    employee_id: Optional[int] = None
    type: str

class AttendanceLateComeEarlyOutRead(HorillaSchema):
    id: int
    attendance_id: int
    type: str
    is_active: bool = True

class GraceTimeCreate(BaseModel):
    allowed_time: str
    allowed_time_in_secs: int
    allowed_clock_in: bool = True
    allowed_clock_out: bool = True
    is_default: bool = False

class GraceTimeRead(HorillaSchema):
    id: int
    allowed_time: str
    is_default: bool
    is_active: bool = True

class AttendanceGeneralSettingCreate(BaseModel):
    time_runner: bool = False
    enable_check_in: bool = True
    company_id: Optional[int] = None

class AttendanceGeneralSettingRead(HorillaSchema):
    id: int
    time_runner: bool
    enable_check_in: bool
    is_active: bool = True

class WorkRecordsCreate(BaseModel):
    record_name: str
    work_record_type: str
    employee_id: int
    date: date
    at_work: str
    min_hour: str
    at_work_second: int
    min_hour_second: int
    note: Optional[str] = None
    message: Optional[str] = None
    is_attendance_record: bool = False
    is_leave_record: bool = False
    attendance_id: Optional[int] = None
    leave_request_id: Optional[int] = None
    shift_id: Optional[int] = None
    day_percentage: float = 1.0

class WorkRecordsRead(HorillaSchema):
    id: int
    record_name: str
    work_record_type: str
    employee_id: int
    date: date
    at_work: str
    min_hour: str

# --- MISSING LEAVE MODELS ---
class AvailableLeaveCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    available_days: float = 0
    carryforward_days: float = 0
    total_leave_days: float = 0
    assigned_date: Optional[date] = None
    reset_date: Optional[date] = None
    expired_date: Optional[date] = None

class AvailableLeaveRead(HorillaSchema):
    id: int
    employee_id: int
    leave_type_id: int
    available_days: float
    total_leave_days: float
    is_active: bool = True

class LeaveAllocationRequestCreate(BaseModel):
    leave_type_id: int
    employee_id: int
    requested_days: float
    requested_date: Optional[date] = None
    description: Optional[str] = None
    attachment: Optional[str] = None
    status: str = "requested"

class LeaveAllocationRequestRead(HorillaSchema):
    id: int
    leave_type_id: int
    employee_id: int
    requested_days: float
    status: str
    is_active: bool = True

class RestrictLeaveCreate(BaseModel):
    title: str
    start_date: date
    end_date: date
    department_id: Optional[int] = None
    include_all: bool = False
    description: Optional[str] = None
    company_id: Optional[int] = None

class RestrictLeaveRead(HorillaSchema):
    id: int
    title: str
    start_date: date
    end_date: date
    include_all: bool
    is_active: bool = True

class CompensatoryLeaveRequestCreate(BaseModel):
    leave_type_id: int
    employee_id: int
    requested_days: float
    requested_date: Optional[date] = None
    description: Optional[str] = None
    status: str = "requested"

class CompensatoryLeaveRequestRead(HorillaSchema):
    id: int
    leave_type_id: int
    employee_id: int
    requested_days: float
    status: str
    is_active: bool = True

# --- MISSING BIOMETRIC MODELS ---
class BiometricEmployeesCreate(BaseModel):
    uid: Optional[int] = None
    ref_user_id: Optional[int] = None
    user_id: Optional[str] = None
    employee_id: int
    device_id: Optional[str] = None

class BiometricEmployeesRead(HorillaSchema):
    id: str
    employee_id: int
    user_id: Optional[str] = None

class FaceDetectionCreate(BaseModel):
    company_id: Optional[int] = None
    start: bool = False

class FaceDetectionRead(HorillaSchema):
    id: int
    company_id: Optional[int] = None
    start: bool

class EmployeeFaceDetectionCreate(BaseModel):
    employee_id: int
    image: Optional[str] = None

class EmployeeFaceDetectionRead(HorillaSchema):
    id: int
    employee_id: int
    image: Optional[str] = None

# --- NEW ADDED SCHEMAS FOR ATTENDANCE ---
class AttendanceRequestFileCreate(BaseModel):
    file: str

class AttendanceRequestFileRead(HorillaSchema):
    id: int
    file: str
    is_active: bool = True

class AttendanceRequestCommentCreate(BaseModel):
    request_id: int
    employee_id: int
    comment: str

class AttendanceRequestCommentRead(HorillaSchema):
    id: int
    request_id: int
    employee_id: int
    comment: str
    is_active: bool = True

class AttendanceValidationConditionCreate(BaseModel):
    validation_at_work: str = "00:00"
    minimum_overtime_to_approve: str = "00:00"
    overtime_cutoff: str = "00:00"
    company_id: Optional[int] = None

class AttendanceValidationConditionRead(HorillaSchema):
    id: int
    validation_at_work: str
    minimum_overtime_to_approve: str
    overtime_cutoff: str
    is_active: bool = True

