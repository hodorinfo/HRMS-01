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
    minimum_hour: str = "00:00"
    is_holiday: bool = False

    @field_validator("attendance_date")
    @classmethod
    def validate_attendance_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Attendance date cannot be in the past")
        return v

class AttendanceUpdate(BaseModel):
    shift_id: Optional[int] = None
    attendance_clock_in: Optional[str] = None
    attendance_clock_out: Optional[str] = None
    attendance_validated: Optional[bool] = None
    attendance_overtime_approve: Optional[bool] = None
    request_description: Optional[str] = None

class AttendanceRead(HorillaSchema):
    id: int
    employee_id: int
    attendance_date: date
    shift_id: Optional[int] = None
    attendance_clock_in: Optional[str] = None
    attendance_clock_out: Optional[str] = None
    attendance_worked_hour: Optional[str] = None
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
