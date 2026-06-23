from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Contract, Allowance, Deduction, Payslip, LoanAccount, FilingStatus, Reimbursement
from app.schemas import (
    ContractCreate, ContractUpdate, ContractRead,
    AllowanceCreate, AllowanceUpdate, AllowanceRead,
    DeductionCreate, DeductionUpdate, DeductionRead,
    PayslipCreate, PayslipUpdate, PayslipRead,
    LoanAccountCreate, LoanAccountRead,
    FilingStatusCreate, FilingStatusUpdate, FilingStatusRead,
    ReimbursementCreate, ReimbursementUpdate, ReimbursementRead,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read, module_name in [
    ("/contracts", Contract, ContractCreate, ContractUpdate, ContractRead, "Contracts"),
    ("/allowances", Allowance, AllowanceCreate, AllowanceUpdate, AllowanceRead, "Allowances"),
    ("/deductions", Deduction, DeductionCreate, DeductionUpdate, DeductionRead, "Deductions"),
    ("/payslips", Payslip, PayslipCreate, PayslipUpdate, PayslipRead, "Payslips"),
    ("/loans", LoanAccount, LoanAccountCreate, LoanAccountCreate, LoanAccountRead, "Loans"),
    ("/filing-status", FilingStatus, FilingStatusCreate, FilingStatusUpdate, FilingStatusRead, "Tax & Filing Status"),
    ("/reimbursements", Reimbursement, ReimbursementCreate, ReimbursementUpdate, ReimbursementRead, "Reimbursements"),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, module_name))

# Register Legacy Actions (Custom Endpoints)
from app.routers import legacy_actions
api_router.include_router(legacy_actions.router)
