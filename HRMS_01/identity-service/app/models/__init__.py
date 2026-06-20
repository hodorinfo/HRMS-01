"""Identity service SQLAlchemy models - mirrors horilla-hr/employee, accessibility, horilla_ldap, outlook_auth."""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from horilla_common.base import Base, HorillaBaseMixin


class User(Base, HorillaBaseMixin):
    __tablename__ = "auth_user"

    username: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_new_employee: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Employee(Base):
    __tablename__ = "employee_employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    badge_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    employee_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("auth_user.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    employee_first_name: Mapped[str] = mapped_column(String(200))
    employee_last_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    employee_profile: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    phone: Mapped[str] = mapped_column(String(25))
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    zip: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default="male")
    qualification: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    marital_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="single")
    children: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    emergency_contact_relation: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    additional_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_from_onboarding: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
    is_directly_converted: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[employee_user_id])
    work_info: Mapped[Optional["EmployeeWorkInformation"]] = relationship(
        "EmployeeWorkInformation", back_populates="employee", uselist=False, foreign_keys="[EmployeeWorkInformation.employee_id]"
    )
    bank_details: Mapped[Optional["EmployeeBankDetails"]] = relationship(
        "EmployeeBankDetails", back_populates="employee", uselist=False
    )


class EmployeeTag(Base, HorillaBaseMixin):
    __tablename__ = "employee_employeetag"
    title: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)


class EmployeeWorkInformation(Base):
    __tablename__ = "employee_employeeworkinformation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("employee_employee.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    department_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_position_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_role_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reporting_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("employee_employee.id", ondelete="SET NULL"), nullable=True
    )
    shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    work_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    employee_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(254), nullable=True)
    mobile: Mapped[Optional[str]] = mapped_column(String(254), nullable=True)
    date_joining: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    contract_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    basic_salary: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    salary_hour: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    additional_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    experience: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)

    employee: Mapped[Optional["Employee"]] = relationship(
        "Employee", back_populates="work_info", foreign_keys=[employee_id]
    )


class EmployeeBankDetails(Base, HorillaBaseMixin):
    __tablename__ = "employee_employeebankdetails"
    employee_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("employee_employee.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    bank_name: Mapped[str] = mapped_column(String(50))
    account_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    branch: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    any_other_code1: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    any_other_code2: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    additional_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    employee: Mapped[Optional["Employee"]] = relationship("Employee", back_populates="bank_details")


class EmployeeNote(Base, HorillaBaseMixin):
    __tablename__ = "employee_employeenote"
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employee_employee.id", ondelete="CASCADE"))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("employee_employee.id"), nullable=True)


class Policy(Base, HorillaBaseMixin):
    __tablename__ = "employee_policy"
    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[str] = mapped_column(Text)
    is_visible_to_all: Mapped[bool] = mapped_column(Boolean, default=True)


class BonusPoint(Base, HorillaBaseMixin):
    __tablename__ = "employee_bonuspoint"
    employee_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("employee_employee.id"), unique=True, nullable=True
    )
    points: Mapped[int] = mapped_column(Integer, default=0)
    encashment_condition: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    redeeming_points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Actiontype(Base, HorillaBaseMixin):
    __tablename__ = "employee_actiontype"
    title: Mapped[str] = mapped_column(String(50))
    action_type: Mapped[str] = mapped_column(String(30))
    block_option: Mapped[bool] = mapped_column(Boolean, default=False)


class DisciplinaryAction(Base, HorillaBaseMixin):
    __tablename__ = "employee_disciplinaryaction"
    action_id: Mapped[int] = mapped_column(Integer, ForeignKey("employee_actiontype.id", ondelete="CASCADE"))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    unit_in: Mapped[str] = mapped_column(String(10), default="days")
    days: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)
    hours: Mapped[str] = mapped_column(String(6), default="00:00")
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    attachment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class EmployeeGeneralSetting(Base, HorillaBaseMixin):
    __tablename__ = "employee_employeegeneralsetting"
    badge_id_prefix: Mapped[str] = mapped_column(String(5), default="PEP")
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class ProfileEditFeature(Base, HorillaBaseMixin):
    __tablename__ = "employee_profileeditfeature"
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)


class DefaultAccessibility(Base, HorillaBaseMixin):
    __tablename__ = "accessibility_defaultaccessibility"
    feature: Mapped[str] = mapped_column(String(100))
    filter: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    exclude_all: Mapped[bool] = mapped_column(Boolean, default=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class LDAPSettings(Base):
    __tablename__ = "horilla_ldap_ldapsettings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ldap_server: Mapped[str] = mapped_column(String(255), default="ldap://127.0.0.1:389")
    bind_dn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bind_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    base_dn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


class AzureApi(Base):
    __tablename__ = "outlook_auth_azureapi"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    outlook_client_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    outlook_client_secret: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    outlook_tenant_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    outlook_email: Mapped[Optional[str]] = mapped_column(String(254), nullable=True)
    outlook_display_name: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    outlook_redirect_uri: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    outlook_authorization_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    outlook_token_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    outlook_api_endpoint: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)
    oauth_state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_refreshed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
