"""Attendance service models."""
from datetime import date, datetime
from typing import Optional
import uuid
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from horilla_common.base import Base, HorillaBaseMixin

class AttendanceActivity(Base, HorillaBaseMixin):
    __tablename__ = "attendance_attendanceactivity"
    employee_id: Mapped[int] = mapped_column(Integer)
    attendance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    shift_day_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    in_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    out_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    clock_in_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    clock_out_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    clock_in: Mapped[str] = mapped_column(String(8))
    clock_out: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

class BatchAttendance(Base, HorillaBaseMixin):
    __tablename__ = "attendance_batchattendance"
    title: Mapped[str] = mapped_column(String(150))

class Attendance(Base, HorillaBaseMixin):
    __tablename__ = "attendance_attendance"
    __table_args__ = (UniqueConstraint("employee_id", "attendance_date", name="uq_employee_date"),)
    employee_id: Mapped[int] = mapped_column(Integer)
    attendance_date: Mapped[date] = mapped_column(Date)
    shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    work_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attendance_day_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attendance_clock_in_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    attendance_clock_in: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    attendance_clock_out_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    attendance_clock_out: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    attendance_worked_hour: Mapped[Optional[str]] = mapped_column(String(10), default="00:00", nullable=True)
    minimum_hour: Mapped[str] = mapped_column(String(10), default="00:00")
    batch_attendance_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attendance_overtime: Mapped[str] = mapped_column(String(10), default="00:00")
    attendance_overtime_approve: Mapped[bool] = mapped_column(Boolean, default=False)
    attendance_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    at_work_second: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    overtime_second: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    approved_overtime_second: Mapped[int] = mapped_column(Integer, default=0)
    is_validate_request: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bulk_request: Mapped[bool] = mapped_column(Boolean, default=False)
    is_validate_request_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    request_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    request_type: Mapped[Optional[str]] = mapped_column(String(18), nullable=True)
    is_holiday: Mapped[bool] = mapped_column(Boolean, default=False)
    requested_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    approved_by_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class AttendanceOverTime(Base, HorillaBaseMixin):
    __tablename__ = "attendance_attendanceovertime"
    employee_id: Mapped[int] = mapped_column(Integer)
    month: Mapped[str] = mapped_column(String(20))
    month_sequence: Mapped[int] = mapped_column(Integer)
    year: Mapped[str] = mapped_column(String(4))
    worked_hours: Mapped[str] = mapped_column(String(10))
    pending_hours: Mapped[str] = mapped_column(String(10))
    overtime: Mapped[str] = mapped_column(String(10))
    hour_account_second: Mapped[int] = mapped_column(Integer)
    hour_pending_second: Mapped[int] = mapped_column(Integer)
    overtime_second: Mapped[int] = mapped_column(Integer)

class AttendanceLateComeEarlyOut(Base, HorillaBaseMixin):
    __tablename__ = "attendance_attendancelatecomeearlyout"
    __table_args__ = (UniqueConstraint("attendance_id", "type", name="uq_attendance_type"),)
    attendance_id: Mapped[int] = mapped_column(Integer, ForeignKey("attendance_attendance.id"))
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(String(20))
    created_at_record: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class GraceTime(Base, HorillaBaseMixin):
    __tablename__ = "attendance_gracetime"
    allowed_time: Mapped[str] = mapped_column(String(10))
    allowed_time_in_secs: Mapped[int] = mapped_column(Integer)
    allowed_clock_in: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_clock_out: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

class AttendanceGeneralSetting(Base, HorillaBaseMixin):
    __tablename__ = "attendance_attendancegeneralsetting"
    time_runner: Mapped[bool] = mapped_column(Boolean, default=False)
    enable_check_in: Mapped[bool] = mapped_column(Boolean, default=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class WorkRecords(Base):
    __tablename__ = "attendance_workrecords"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    record_name: Mapped[str] = mapped_column(String(100))
    work_record_type: Mapped[str] = mapped_column(String(20))
    employee_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[date] = mapped_column(Date)
    at_work: Mapped[str] = mapped_column(String(10))
    min_hour: Mapped[str] = mapped_column(String(10))
    at_work_second: Mapped[int] = mapped_column(Integer)
    min_hour_second: Mapped[int] = mapped_column(Integer)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    message: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    is_attendance_record: Mapped[bool] = mapped_column(Boolean, default=False)
    is_leave_record: Mapped[bool] = mapped_column(Boolean, default=False)
    attendance_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    leave_request_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    day_percentage: Mapped[float] = mapped_column(Float, default=1.0)
    last_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

# Leave models
class LeaveType(Base, HorillaBaseMixin):
    __tablename__ = "leave_leavetype"
    name: Mapped[str] = mapped_column(String(50))
    color: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    payment: Mapped[str] = mapped_column(String(10), default="paid")
    count: Mapped[float] = mapped_column(Float, default=0)
    period_in: Mapped[str] = mapped_column(String(10), default="day")
    limit_leave: Mapped[bool] = mapped_column(Boolean, default=False)
    reset: Mapped[bool] = mapped_column(Boolean, default=False)
    is_encashable: Mapped[bool] = mapped_column(Boolean, default=False)
    require_approval: Mapped[str] = mapped_column(String(3), default="yes")
    require_attachment: Mapped[str] = mapped_column(String(3), default="no")
    exclude_company_leave: Mapped[str] = mapped_column(String(3), default="no")
    exclude_holiday: Mapped[str] = mapped_column(String(3), default="no")
    is_compensatory_leave: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class AvailableLeave(Base, HorillaBaseMixin):
    __tablename__ = "leave_availableleave"
    employee_id: Mapped[int] = mapped_column(Integer)
    leave_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("leave_leavetype.id"))
    available_days: Mapped[float] = mapped_column(Float, default=0)
    carryforward_days: Mapped[float] = mapped_column(Float, default=0)
    total_leave_days: Mapped[float] = mapped_column(Float, default=0)
    assigned_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    reset_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expired_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

class LeaveRequest(Base, HorillaBaseMixin):
    __tablename__ = "leave_leaverequest"
    employee_id: Mapped[int] = mapped_column(Integer)
    leave_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("leave_leavetype.id"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    start_date_breakdown: Mapped[str] = mapped_column(String(20), default="full_day")
    end_date_breakdown: Mapped[str] = mapped_column(String(20), default="full_day")
    requested_days: Mapped[float] = mapped_column(Float)
    leave_clashes_count: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    requested_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    approved_available_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    approved_carryforward_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class LeaveAllocationRequest(Base, HorillaBaseMixin):
    __tablename__ = "leave_leaveallocationrequest"
    leave_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("leave_leavetype.id"))
    employee_id: Mapped[int] = mapped_column(Integer)
    requested_days: Mapped[float] = mapped_column(Float)
    requested_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class RestrictLeave(Base, HorillaBaseMixin):
    __tablename__ = "leave_restrictleave"
    title: Mapped[str] = mapped_column(String(50))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    department_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    include_all: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class CompensatoryLeaveRequest(Base, HorillaBaseMixin):
    __tablename__ = "leave_compensatoryleaverequest"
    leave_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("leave_leavetype.id"))
    employee_id: Mapped[int] = mapped_column(Integer)
    requested_days: Mapped[float] = mapped_column(Float)
    requested_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    reject_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# Biometric
class BiometricDevices(Base, HorillaBaseMixin):
    __tablename__ = "biometric_biometricdevices"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100))
    machine_type: Mapped[str] = mapped_column(String(20))
    machine_ip: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    zk_password: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    bio_username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    bio_password: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False)
    is_scheduler: Mapped[bool] = mapped_column(Boolean, default=False)
    scheduler_duration: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_fetch_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    last_fetch_time: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    device_direction: Mapped[str] = mapped_column(String(20), default="system")
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class BiometricEmployees(Base):
    __tablename__ = "biometric_biometricemployees"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uid: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ref_user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    employee_id: Mapped[int] = mapped_column(Integer)
    device_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("biometric_biometricdevices.id"), nullable=True)

# Geofencing
class GeoFencing(Base):
    __tablename__ = "geofencing_geofencing"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    radius_in_meters: Mapped[int] = mapped_column(Integer)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    start: Mapped[bool] = mapped_column(Boolean, default=False)

# Face Detection
class FaceDetection(Base):
    __tablename__ = "facedetection_facedetection"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    start: Mapped[bool] = mapped_column(Boolean, default=False)

class EmployeeFaceDetection(Base):
    __tablename__ = "facedetection_employeefacedetection"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, unique=True)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
