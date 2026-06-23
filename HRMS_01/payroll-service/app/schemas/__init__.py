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

class FilingStatusCreate(BaseModel):
    filing_status: str
    based_on: str
    use_py: bool = False
    python_code: Optional[str] = None
    description: Optional[str] = None
    company_id: Optional[int] = None

class FilingStatusUpdate(BaseModel):
    filing_status: Optional[str] = None
    based_on: Optional[str] = None
    use_py: Optional[bool] = None

class FilingStatusRead(HorillaSchema):
    id: int
    filing_status: str
    based_on: str
    use_py: bool
    is_active: bool = True

class ReimbursementCreate(BaseModel):
    title: str
    type: str
    employee_id: int
    amount: float = 0
    status: str = "requested"

class ReimbursementUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None

class ReimbursementRead(HorillaSchema):
    id: int
    title: str
    type: str
    employee_id: int
    amount: float
    status: str
    is_active: bool = True
