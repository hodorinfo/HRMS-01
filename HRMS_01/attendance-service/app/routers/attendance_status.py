from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict
from datetime import date

from app.database import get_db
from app.dependencies import get_current_user
from app.models import AttendanceActivity

router = APIRouter()

@router.get("/status", response_model=Dict[int, bool])
async def get_attendance_status(
    employee_ids: str = Query(..., description="Comma-separated list of employee IDs"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get the current online/offline status of a list of employees.
    Returns a dictionary mapping employee_id to a boolean (True if online, False if offline).
    """
    if not employee_ids:
        return {}
        
    try:
        # Convert comma-separated string to list of integers
        id_list = [int(eid.strip()) for eid in employee_ids.split(",") if eid.strip().isdigit()]
    except ValueError:
        return {}

    if not id_list:
        return {}

    today = date.today()

    # Query the latest AttendanceActivity for each requested employee for today
    # We use a subquery or a distinct/group by approach.
    # In SQLite/Postgres, getting the latest record per employee can be done by ordering.
    # A simple and cross-db compatible way for a small list of IDs is to query all activities
    # for these IDs today, and manually sort/process them, since a single day's punches per employee are very few.
    
    # Use async select
    stmt = select(AttendanceActivity).where(
        AttendanceActivity.employee_id.in_(id_list),
        AttendanceActivity.attendance_date == today
    ).order_by(AttendanceActivity.employee_id, AttendanceActivity.in_datetime.desc())
    
    result = await db.scalars(stmt)
    activities = result.all()

    # Process activities to find the latest state
    # Since they are ordered by in_datetime desc, the first one we encounter for an employee is the latest.
    latest_status = {}
    processed_ids = set()

    for activity in activities:
        if activity.employee_id not in processed_ids:
            # If there is a clock_in but NO clock_out, they are online.
            is_online = (activity.clock_in is not None and activity.clock_out is None)
            latest_status[activity.employee_id] = is_online
            processed_ids.add(activity.employee_id)

    # For employees that didn't have any activity today, they are offline (False)
    result = {}
    for eid in id_list:
        result[eid] = latest_status.get(eid, False)

    return result
