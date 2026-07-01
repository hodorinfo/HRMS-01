"""Core service models - mirrors horilla-hr/base."""
from datetime import date
from typing import Optional
from sqlalchemy import Boolean, Date, ForeignKey, Integer, JSON, String, Text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from horilla_common.base import Base, HorillaBaseMixin

company_department = Table("base_department_company_id", Base.metadata,
    Column("department_id", Integer, ForeignKey("base_department.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", Integer, ForeignKey("base_company.id", ondelete="CASCADE"), primary_key=True))

class Company(Base, HorillaBaseMixin):
    __tablename__ = "base_company"
    company: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(Text)
    country: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    zip: Mapped[str] = mapped_column(String(20))
    icon: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    date_format: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    time_format: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

class Department(Base, HorillaBaseMixin):
    __tablename__ = "base_department"
    department: Mapped[str] = mapped_column(String(50))
    companies: Mapped[list["Company"]] = relationship("Company", secondary=company_department)

class JobPosition(Base, HorillaBaseMixin):
    __tablename__ = "base_jobposition"
    job_position: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_department.id", ondelete="RESTRICT"))

class JobRole(Base, HorillaBaseMixin):
    __tablename__ = "base_jobrole"
    job_position_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_jobposition.id", ondelete="RESTRICT"))
    job_role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

class WorkType(Base, HorillaBaseMixin):
    __tablename__ = "base_worktype"
    work_type: Mapped[str] = mapped_column(String(50))

class EmployeeType(Base, HorillaBaseMixin):
    __tablename__ = "base_employeetype"
    employee_type: Mapped[str] = mapped_column(String(50))

class EmployeeShiftDay(Base):
    __tablename__ = "base_employeeshiftday"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day: Mapped[str] = mapped_column(String(20))

class EmployeeShift(Base, HorillaBaseMixin):
    __tablename__ = "base_employeeshift"
    employee_shift: Mapped[str] = mapped_column(String(50))
    weekly_full_time: Mapped[Optional[str]] = mapped_column(String(6), default="40:00", nullable=True)
    full_time: Mapped[str] = mapped_column(String(6), default="200:00")
    grace_time_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class EmployeeShiftSchedule(Base, HorillaBaseMixin):
    __tablename__ = "base_employeeshiftschedule"
    day_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_employeeshiftday.id"))
    shift_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_employeeshift.id"))
    minimum_working_hour: Mapped[str] = mapped_column(String(5), default="08:15")
    start_time: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    end_time: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    is_night_shift: Mapped[bool] = mapped_column(Boolean, default=False)
    is_auto_punch_out_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_punch_out_time: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

class RotatingWorkType(Base, HorillaBaseMixin):
    __tablename__ = "base_rotatingworktype"
    name: Mapped[str] = mapped_column(String(50))
    work_type1_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_worktype.id"))
    work_type2_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_worktype.id"))
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)

class RotatingWorkTypeAssign(Base, HorillaBaseMixin):
    __tablename__ = "base_rotatingworktypeassign"
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rotating_work_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_rotatingworktype.id"))
    start_date: Mapped[date] = mapped_column(Date)
    next_change_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    current_work_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    next_work_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    based_on: Mapped[str] = mapped_column(String(10))
    rotate_after_day: Mapped[int] = mapped_column(Integer, default=7)
    rotate_every_weekend: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    rotate_every: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class RotatingShift(Base, HorillaBaseMixin):
    __tablename__ = "base_rotatingshift"
    name: Mapped[str] = mapped_column(String(50))
    shift1_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_employeeshift.id"))
    shift2_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_employeeshift.id"))
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)

class RotatingShiftAssign(Base, HorillaBaseMixin):
    __tablename__ = "base_rotatingshiftassign"
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rotating_shift_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_rotatingshift.id"))
    start_date: Mapped[date] = mapped_column(Date)
    next_change_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    current_shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    next_shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    based_on: Mapped[str] = mapped_column(String(10))
    rotate_after_day: Mapped[int] = mapped_column(Integer, default=7)
    rotate_every_weekend: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    rotate_every: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class WorkTypeRequest(Base, HorillaBaseMixin):
    __tablename__ = "base_worktyperequest"
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    work_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_worktype.id"))
    previous_work_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    requested_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    requested_till: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_permanent_work_type: Mapped[bool] = mapped_column(Boolean, default=False)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    canceled: Mapped[bool] = mapped_column(Boolean, default=False)
    work_type_changed: Mapped[bool] = mapped_column(Boolean, default=False)

class ShiftRequest(Base, HorillaBaseMixin):
    __tablename__ = "base_shiftrequest"
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    shift_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_employeeshift.id"))
    previous_shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    requested_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    requested_till: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_permanent_shift: Mapped[bool] = mapped_column(Boolean, default=False)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    canceled: Mapped[bool] = mapped_column(Boolean, default=False)
    shift_changed: Mapped[bool] = mapped_column(Boolean, default=False)

class ShiftRequestComment(Base, HorillaBaseMixin):
    __tablename__ = "base_shiftrequestcomment"
    request_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_shiftrequest.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class Holidays(Base, HorillaBaseMixin):
    __tablename__ = "base_holidays"
    name: Mapped[str] = mapped_column(String(30))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    recurring: Mapped[bool] = mapped_column(Boolean, default=False)

class CompanyLeaves(Base, HorillaBaseMixin):
    __tablename__ = "base_companyleaves"
    based_on_week: Mapped[str] = mapped_column(String(1))
    based_on_week_day: Mapped[str] = mapped_column(String(1))

class MultipleApprovalCondition(Base, HorillaBaseMixin):
    __tablename__ = "base_multipleapprovalcondition"
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_department.id", ondelete="CASCADE"))
    condition_field: Mapped[str] = mapped_column(String(50))
    condition_operator: Mapped[str] = mapped_column(String(20))
    condition_value: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    condition_start_value: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    condition_end_value: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

class MultipleApprovalManagers(Base):
    __tablename__ = "base_multipleapprovalmanagers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    condition_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_multipleapprovalcondition.id", ondelete="CASCADE"))
    sequence: Mapped[int] = mapped_column(Integer)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reporting_manager: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

class Announcement(Base, HorillaBaseMixin):
    __tablename__ = "base_announcement"
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disable_comments: Mapped[bool] = mapped_column(Boolean, default=False)
    public_comments: Mapped[bool] = mapped_column(Boolean, default=True)

class AnnouncementComment(Base, HorillaBaseMixin):
    __tablename__ = "base_announcementcomment"
    announcement_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_announcement.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class AnnouncementView(Base, HorillaBaseMixin):
    __tablename__ = "base_announcementview"
    announcement_id: Mapped[int] = mapped_column(Integer, ForeignKey("base_announcement.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(Integer)
    viewed: Mapped[bool] = mapped_column(Boolean, default=False)

class HorillaMailTemplate(Base, HorillaBaseMixin):
    __tablename__ = "base_horillamailtemplate"
    title: Mapped[str] = mapped_column(String(100), unique=True)
    body: Mapped[str] = mapped_column(Text)
