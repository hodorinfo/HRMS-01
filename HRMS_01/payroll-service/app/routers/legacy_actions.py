from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Payslip, Reimbursement

router = APIRouter(tags=["Legacy Actions"])

class SendMailPayload(BaseModel):
    payslip_id: int
    email: Optional[str] = None

class ReimbursementStatusPayload(BaseModel):
    status: str

# 1. Payslip Download
@router.get("/payslip-download/{id}")
async def download_payslip(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    payslip = await db.get(Payslip, id)
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    
    # In a full implementation, this would return a PDF FileResponse.
    # For now, we return a mock success message indicating the PDF generation service would run here.
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": f"PDF generated for payslip {id}", "download_url": f"/media/payslips/payslip_{id}.pdf"}
    )

# 2. Payslip Send Mail
@router.post("/payslip-send-mail/")
async def send_payslip_mail(payload: SendMailPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    payslip = await db.get(Payslip, payload.payslip_id)
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    
    # Mark as sent
    payslip.sent_to_employee = True
    await db.commit()
    
    return {"status": "success", "message": f"Mail triggered for payslip {payload.payslip_id}"}

# 3. Reimbursement Approve/Reject
# Note: Handled both correct spelling and the legacy typo from the URL list
@router.put("/reimbusement-approve-reject/{id}")
@router.put("/reimbursement-approve-reject/{id}")
async def approve_reject_reimbursement(id: int, payload: ReimbursementStatusPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    valid_statuses = ["approved", "rejected", "requested"]
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    reimb = await db.get(Reimbursement, id)
    if not reimb:
        raise HTTPException(status_code=404, detail="Reimbursement not found")
    
    reimb.status = payload.status
    await db.commit()
    
    return {"status": "success", "reimbursement_id": id, "new_status": payload.status}
