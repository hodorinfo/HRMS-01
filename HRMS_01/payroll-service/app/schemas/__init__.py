from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ContractCreate(BaseModel):
    contract_name: str
    employee_id: int
    contract_start_date: date
    contract_end_date: Optional[date] = None
    wage_type: str
    pay_frequency: str
    wage: float
    filing_status_id: Optional[int] = None
    contract_status: str = "draft"

class ContractUpdate(BaseModel):
    contract_name: Optional[str] = None
    contract_end_date: Optional[date] = None
    wage: Optional[float] = None
    contract_status: Optional[str] = None

class ContractRead(HorillaSchema):
    id: int
    contract_name: str
    employee_id: int
    contract_start_date: date
    wage_type: str
    pay_frequency: str
    wage: float
    contract_status: str
    is_active: bool = True

class AllowanceCreate(BaseModel):
    title: str
    amount: float = 0
    is_taxable: bool = False
    is_fixed: bool = True
    company_id: Optional[int] = None

class AllowanceUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None

class AllowanceRead(HorillaSchema):
    id: int
    title: str
    amount: float
    is_taxable: bool
    is_active: bool = True

class DeductionCreate(BaseModel):
    title: str
    amount: float = 0
    is_tax: bool = False
    is_fixed: bool = True
    company_id: Optional[int] = None

class DeductionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None

class DeductionRead(HorillaSchema):
    id: int
    title: str
    amount: float
    is_tax: bool
    is_active: bool = True

class PayslipCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    contract_wage: float = 0
    basic_pay: float = 0
    gross_pay: float = 0
    deduction: float = 0
    net_pay: float = 0

class PayslipUpdate(BaseModel):
    status: Optional[str] = None
    sent_to_employee: Optional[bool] = None

class PayslipRead(HorillaSchema):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    gross_pay: float
    net_pay: float
    status: str
    is_active: bool = True

class LoanAccountCreate(BaseModel):
    type: str
    title: str
    employee_id: int
    loan_amount: float
    provided_date: date
    installment_amount: float = 0
    installments: int = 0

class LoanAccountRead(HorillaSchema):
    id: int
    type: str
    title: str
    employee_id: int
    loan_amount: float
    settled: bool = False
    is_active: bool = True
