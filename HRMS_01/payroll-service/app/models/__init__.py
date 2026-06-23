from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from horilla_common.base import Base, HorillaBaseMixin

class FilingStatus(Base, HorillaBaseMixin):
    __tablename__ = "payroll_filingstatus"
    filing_status: Mapped[str] = mapped_column(String(30))
    based_on: Mapped[str] = mapped_column(String(30))
    use_py: Mapped[bool] = mapped_column(Boolean, default=False)
    python_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class Contract(Base, HorillaBaseMixin):
    __tablename__ = "payroll_contract"
    contract_name: Mapped[str] = mapped_column(String(100))
    employee_id: Mapped[int] = mapped_column(Integer, unique=True)
    contract_start_date: Mapped[date] = mapped_column(Date)
    contract_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    wage_type: Mapped[str] = mapped_column(String(20))
    pay_frequency: Mapped[str] = mapped_column(String(20))
    wage: Mapped[float] = mapped_column(Float)
    filing_status_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("payroll_filingstatus.id"), nullable=True)
    contract_status: Mapped[str] = mapped_column(String(20), default="draft")
    department_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_position_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_role_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    shift_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    work_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notice_period_in_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    contract_document: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    deduct_leave_from_basic_pay: Mapped[bool] = mapped_column(Boolean, default=False)
    calculate_daily_leave_amount: Mapped[bool] = mapped_column(Boolean, default=False)
    deduction_for_one_leave_amount: Mapped[float] = mapped_column(Float, default=0)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class Allowance(Base, HorillaBaseMixin):
    __tablename__ = "payroll_allowance"
    title: Mapped[str] = mapped_column(String(100))
    one_time_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    include_active_employees: Mapped[bool] = mapped_column(Boolean, default=False)
    is_taxable: Mapped[bool] = mapped_column(Boolean, default=False)
    is_condition_based: Mapped[bool] = mapped_column(Boolean, default=False)
    is_fixed: Mapped[bool] = mapped_column(Boolean, default=True)
    field: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    condition: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    value: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount: Mapped[float] = mapped_column(Float, default=0)
    based_on: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_loan: Mapped[bool] = mapped_column(Boolean, default=False)

class Deduction(Base, HorillaBaseMixin):
    __tablename__ = "payroll_deduction"
    title: Mapped[str] = mapped_column(String(100))
    one_time_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    include_active_employees: Mapped[bool] = mapped_column(Boolean, default=False)
    is_tax: Mapped[bool] = mapped_column(Boolean, default=False)
    is_pretax: Mapped[bool] = mapped_column(Boolean, default=False)
    is_condition_based: Mapped[bool] = mapped_column(Boolean, default=False)
    is_fixed: Mapped[bool] = mapped_column(Boolean, default=True)
    field: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    condition: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    value: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount: Mapped[float] = mapped_column(Float, default=0)
    based_on: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    update_compensation: Mapped[bool] = mapped_column(Boolean, default=False)
    employer_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_installment: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class Payslip(Base, HorillaBaseMixin):
    __tablename__ = "payroll_payslip"
    group_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    employee_id: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    pay_head_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    contract_wage: Mapped[float] = mapped_column(Float, default=0)
    basic_pay: Mapped[float] = mapped_column(Float, default=0)
    gross_pay: Mapped[float] = mapped_column(Float, default=0)
    deduction: Mapped[float] = mapped_column(Float, default=0)
    net_pay: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    sent_to_employee: Mapped[bool] = mapped_column(Boolean, default=False)

class LoanAccount(Base, HorillaBaseMixin):
    __tablename__ = "payroll_loanaccount"
    type: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(100))
    employee_id: Mapped[int] = mapped_column(Integer)
    loan_amount: Mapped[float] = mapped_column(Float)
    provided_date: Mapped[date] = mapped_column(Date)
    allowance_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_fixed: Mapped[bool] = mapped_column(Boolean, default=True)
    rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    installment_amount: Mapped[float] = mapped_column(Float, default=0)
    installments: Mapped[int] = mapped_column(Integer, default=0)
    installment_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    settled: Mapped[bool] = mapped_column(Boolean, default=False)
    settled_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class Reimbursement(Base, HorillaBaseMixin):
    __tablename__ = "payroll_reimbursement"
    title: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(30))
    employee_id: Mapped[int] = mapped_column(Integer)
    allowance_on: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    amount: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    approved_by_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
