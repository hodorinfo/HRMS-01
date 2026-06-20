from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Contract, Allowance, Deduction, Payslip, LoanAccount, FilingStatus
from app.schemas import (
    ContractCreate, ContractUpdate, ContractRead,
    AllowanceCreate, AllowanceUpdate, AllowanceRead,
    DeductionCreate, DeductionUpdate, DeductionRead,
    PayslipCreate, PayslipUpdate, PayslipRead,
    LoanAccountCreate, LoanAccountRead,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read in [
    ("/contracts", Contract, ContractCreate, ContractUpdate, ContractRead),
    ("/allowances", Allowance, AllowanceCreate, AllowanceUpdate, AllowanceRead),
    ("/deductions", Deduction, DeductionCreate, DeductionUpdate, DeductionRead),
    ("/payslips", Payslip, PayslipCreate, PayslipUpdate, PayslipRead),
    ("/loans", LoanAccount, LoanAccountCreate, LoanAccountCreate, LoanAccountRead),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, "payroll"))
