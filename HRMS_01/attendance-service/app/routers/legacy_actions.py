from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.database import get_db
from app.dependencies import get_current_user
from app.models import (
    Attendance, AttendanceActivity, AttendanceOverTime, LeaveRequest, LeaveAllocationRequest
)

router = APIRouter(tags=["Legacy Actions"])

class AttendanceRequestPayload(BaseModel):
    employee_id: int
    attendance_date: date
    attendance_clock_in_date: Optional[date] = None
    attendance_clock_in: Optional[str] = None
    attendance_clock_out_date: Optional[date] = None
    attendance_clock_out: Optional[str] = None
    request_description: Optional[str] = None
    shift_id: Optional[int] = None
    work_type_id: Optional[int] = None
    minimum_hour: str = "00:00"

@router.get("/attendance-request")
async def get_attendance_requests(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Returns all attendances that are validate requests
    stmt = select(Attendance).where(Attendance.is_validate_request == True)
    results = await db.scalars(stmt)
    return results.all()

@router.get("/attendance-request/{id}")
async def get_attendance_request(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    attendance = await db.get(Attendance, id)
    if not attendance or not attendance.is_validate_request:
        raise HTTPException(status_code=404, detail="Attendance request not found")
    return attendance

@router.post("/attendance-request", status_code=status.HTTP_201_CREATED)
async def create_attendance_request(payload: AttendanceRequestPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if attendance already exists
    stmt = select(Attendance).where(
        Attendance.employee_id == payload.employee_id,
        Attendance.attendance_date == payload.attendance_date
    )
    result = await db.scalars(stmt)
    existing_attendance = result.first()

    if existing_attendance:
        # Convert payload to dict for requested_data
        import json
        payload_dict = payload.dict()
        for k, v in payload_dict.items():
            if isinstance(v, date):
                payload_dict[k] = v.isoformat()
        
        existing_attendance.requested_data = json.dumps(payload_dict)
        existing_attendance.is_validate_request = True
        existing_attendance.request_type = "update_request"
        existing_attendance.request_description = payload.request_description
        await db.commit()
        return existing_attendance

    # Create new attendance request
    new_attendance = Attendance(
        **payload.dict(exclude_none=True),
        is_validate_request=True,
        attendance_validated=False,
        request_type="create_request"
    )
    db.add(new_attendance)
    await db.commit()
    await db.refresh(new_attendance)
    return new_attendance

@router.put("/attendance-request/{id}")
async def update_attendance_request(id: int, payload: AttendanceRequestPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    attendance = await db.get(Attendance, id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    import json
    payload_dict = payload.dict()
    for k, v in payload_dict.items():
        if isinstance(v, date):
            payload_dict[k] = v.isoformat()
            
    attendance.requested_data = json.dumps(payload_dict)
    attendance.is_validate_request = True
    attendance.request_type = "update_request"
    attendance.request_description = payload.request_description
    await db.commit()
    return attendance

class ClockInOutPayload(BaseModel):
    employee_id: int

class ActionPayload(BaseModel):
    status: str

class BulkActionPayload(BaseModel):
    ids: List[int]
    action: str

# 1. Clock In
@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
async def clock_in(payload: ClockInOutPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow()
    today = now.date()
    current_time = now.strftime("%H:%M:%S")

    # Log activity
    activity = AttendanceActivity(
        employee_id=payload.employee_id,
        attendance_date=today,
        clock_in=current_time,
        in_datetime=now,
        clock_in_date=today
    )
    db.add(activity)

    # Update or create Attendance
    stmt = select(Attendance).where(
        Attendance.employee_id == payload.employee_id,
        Attendance.attendance_date == today
    )
    result = await db.scalars(stmt)
    attendance = result.first()

    if not attendance:
        attendance = Attendance(
            employee_id=payload.employee_id,
            attendance_date=today,
            attendance_clock_in=current_time,
            attendance_clock_in_date=today
        )
        db.add(attendance)
    elif not attendance.attendance_clock_in:
        attendance.attendance_clock_in = current_time
        attendance.attendance_clock_in_date = today

    await db.commit()
    return {"status": "clocked_in", "time": current_time}

# 2. Clock Out
@router.post("/clock-out", status_code=status.HTTP_200_OK)
async def clock_out(payload: ClockInOutPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow()
    today = now.date()
    current_time = now.strftime("%H:%M:%S")

    # Update latest activity
    stmt = select(AttendanceActivity).where(
        AttendanceActivity.employee_id == payload.employee_id,
        AttendanceActivity.attendance_date == today
    ).order_by(AttendanceActivity.id.desc())
    result = await db.scalars(stmt)
    activity = result.first()
    if activity and not activity.clock_out:
        activity.clock_out = current_time
        activity.out_datetime = now
        activity.clock_out_date = today

    # Update Attendance
    stmt_att = select(Attendance).where(
        Attendance.employee_id == payload.employee_id,
        Attendance.attendance_date == today
    )
    result_att = await db.scalars(stmt_att)
    attendance = result_att.first()
    if attendance:
        attendance.attendance_clock_out = current_time
        attendance.attendance_clock_out_date = today

    await db.commit()
    return {"status": "clocked_out", "time": current_time}

# 3. Attendance Validations
@router.put("/attendance-validate/{id}")
async def validate_attendance(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    attendance = await db.get(Attendance, id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    attendance.attendance_validated = True
    await db.commit()
    return {"status": "validated"}

@router.put("/attendance-request-approve/{id}")
async def approve_attendance_request(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    attendance = await db.get(Attendance, id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    attendance.is_validate_request_approved = True
    await db.commit()
    return {"status": "approved"}

@router.put("/attendance-request-cancel/{id}")
async def cancel_attendance_request(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    attendance = await db.get(Attendance, id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    attendance.is_validate_request_approved = False
    await db.commit()
    return {"status": "cancelled"}

@router.put("/overtime-approve/{id}")
async def approve_overtime(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    attendance = await db.get(Attendance, id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    attendance.attendance_overtime_approve = True
    if attendance.overtime_second:
        attendance.approved_overtime_second = attendance.overtime_second
    await db.commit()
    return {"status": "overtime_approved"}

# 4. Leave Approvals
@router.put("/approve/{id}")
async def approve_leave(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    leave = await db.get(LeaveRequest, id)
    if not leave:
        raise HTTPException(status_code=404, detail="LeaveRequest not found")
    leave.status = "approved"
    await db.commit()
    return {"status": "approved"}

@router.put("/reject/{id}")
async def reject_leave(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    leave = await db.get(LeaveRequest, id)
    if not leave:
        raise HTTPException(status_code=404, detail="LeaveRequest not found")
    leave.status = "rejected"
    await db.commit()
    return {"status": "rejected"}

@router.put("/cancel/{id}")
async def cancel_leave(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    leave = await db.get(LeaveRequest, id)
    if not leave:
        raise HTTPException(status_code=404, detail="LeaveRequest not found")
    leave.status = "cancelled"
    await db.commit()
    return {"status": "cancelled"}

# 5. Allocation Approvals
@router.put("/allocation-approve/{id}")
async def approve_allocation(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    alloc = await db.get(LeaveAllocationRequest, id)
    if not alloc:
        raise HTTPException(status_code=404, detail="Allocation not found")
    alloc.status = "approved"
    await db.commit()
    return {"status": "approved"}

@router.put("/allocation-reject/{id}")
async def reject_allocation(id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    alloc = await db.get(LeaveAllocationRequest, id)
    if not alloc:
        raise HTTPException(status_code=404, detail="Allocation not found")
    alloc.status = "rejected"
    await db.commit()
    return {"status": "rejected"}

# 6. Bulk Actions
@router.post("/request-bulk-action")
async def bulk_leave_action(payload: BulkActionPayload, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    valid_actions = ["approved", "rejected", "cancelled", "deleted"]
    if payload.action not in valid_actions:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    if payload.action == "deleted":
        stmt = select(LeaveRequest).where(LeaveRequest.id.in_(payload.ids))
        results = await db.scalars(stmt)
        for leave in results:
            leave.is_active = False
    else:
        stmt = select(LeaveRequest).where(LeaveRequest.id.in_(payload.ids))
        results = await db.scalars(stmt)
        for leave in results:
            leave.status = payload.action
            
    await db.commit()
    return {"status": "success", "updated_ids": payload.ids, "action": payload.action}

# 7. Dashboard Endpoints
@router.get("/offline-employees/count")
async def get_offline_count(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"count": 0}

@router.get("/offline-employees/list")
async def get_offline_list(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return {"results": []}
