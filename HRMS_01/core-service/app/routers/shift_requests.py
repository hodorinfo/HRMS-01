"""Shift request bulk action, list, approve/reject endpoints."""

from datetime import date
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models import ShiftRequest
from app.schemas.shiftrequest import (
    BulkIdsRequest,
    BulkActionResponse,
    ShiftRequestCreate,
    ShiftRequestUpdate,
    ShiftRequestRead,
)
from horilla_common.schemas import PaginatedResponse
from app.config import get_settings

router = APIRouter(prefix="/shift-requests", tags=["base"])


async def _update_employee_shift(employee_id: int, new_shift_id: int, auth_header: str) -> None:
    """Call identity-service to update an employee's work_info shift_id.

    Raises HTTPException(502) if the identity-service call fails.
    """
    settings = get_settings()
    identity_base = settings.identity_service_url.rstrip("/")

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Fetch work_info by employee_id
        wi_resp = await client.get(
            f"{identity_base}/api/v1/employees/{employee_id}/work-info",
            headers={"Authorization": auth_header},
        )
        if wi_resp.status_code == 404:
            raise HTTPException(
                status_code=502,
                detail=f"Work information not found for employee #{employee_id}",
            )
        if wi_resp.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch employee work info: {wi_resp.text}",
            )

        work_info = wi_resp.json()
        work_info_id = work_info["id"]

        # 2. Update shift_id on work_info
        update_resp = await client.put(
            f"{identity_base}/api/v1/employees/work-info/{work_info_id}",
            json={"shift_id": new_shift_id},
            headers={"Authorization": auth_header, "Content-Type": "application/json"},
        )
        if update_resp.status_code not in (200, 201):
            raise HTTPException(
                status_code=502,
                detail=f"Failed to update employee shift: {update_resp.text}",
            )


async def _reject_shift_request(
    shift_req: ShiftRequest, db: AsyncSession
) -> ShiftRequest:
    """Shared helper: mark a shift request as rejected (no cross-service call)."""
    shift_req.canceled = True
    shift_req.approved = False
    await db.flush()
    await db.refresh(shift_req)
    return shift_req


async def _approve_shift_request(
    shift_req: ShiftRequest, auth_header: str, db: AsyncSession
) -> ShiftRequest:
    """Shared helper: update employee shift via identity-service, then mark request as approved.

    This function is designed to be reused by both single-request approve
    and future bulk-approve endpoints.
    """
    await _update_employee_shift(shift_req.employee_id, shift_req.shift_id, auth_header)
    shift_req.approved = True
    shift_req.canceled = False
    shift_req.shift_changed = True
    await db.flush()
    await db.refresh(shift_req)
    return shift_req


@router.get("", response_model=PaginatedResponse[ShiftRequestRead])
async def list_shift_requests(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    employee_id: Optional[int] = None,
    shift_id: Optional[int] = None,
    previous_shift_id: Optional[int] = None,
    approved: Optional[bool] = None,
    canceled: Optional[bool] = None,
    shift_changed: Optional[bool] = None,
    is_active: Optional[bool] = None,
    is_permanent_shift: Optional[bool] = None,
    requested_date_from: Optional[date] = None,
    requested_date_to: Optional[date] = None,
    requested_till_from: Optional[date] = None,
    requested_till_to: Optional[date] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.view_shiftrequest")),
):
    query = select(ShiftRequest)

    if search:
        query = query.where(ShiftRequest.description.ilike(f"%{search}%"))
    if employee_id is not None:
        query = query.where(ShiftRequest.employee_id == employee_id)
    if shift_id is not None:
        query = query.where(ShiftRequest.shift_id == shift_id)
    if previous_shift_id is not None:
        query = query.where(ShiftRequest.previous_shift_id == previous_shift_id)
    if approved is not None:
        query = query.where(ShiftRequest.approved == approved)
    if canceled is not None:
        query = query.where(ShiftRequest.canceled == canceled)
    if shift_changed is not None:
        query = query.where(ShiftRequest.shift_changed == shift_changed)
    if is_active is not None:
        query = query.where(ShiftRequest.is_active == is_active)
    if is_permanent_shift is not None:
        query = query.where(ShiftRequest.is_permanent_shift == is_permanent_shift)
    if requested_date_from is not None:
        query = query.where(ShiftRequest.requested_date >= requested_date_from)
    if requested_date_to is not None:
        query = query.where(ShiftRequest.requested_date <= requested_date_to)
    if requested_till_from is not None:
        query = query.where(ShiftRequest.requested_till >= requested_till_from)
    if requested_till_to is not None:
        query = query.where(ShiftRequest.requested_till <= requested_till_to)
    if description:
        query = query.where(ShiftRequest.description.ilike(f"%{description}%"))

    if status:
        if status == "requested":
            query = query.where(
                and_(
                    ShiftRequest.approved == False,
                    ShiftRequest.canceled == False,
                )
            )
        elif status == "approved":
            query = query.where(ShiftRequest.approved == True)
        elif status == "rejected":
            query = query.where(ShiftRequest.canceled == True)
        elif status == "shift_changed":
            query = query.where(ShiftRequest.shift_changed == True)

    total = await db.scalar(
        select(func.count()).select_from(ShiftRequest).where(query.whereclause)
        if query.whereclause is not None
        else select(func.count()).select_from(ShiftRequest)
    )
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        items=[ShiftRequestRead.model_validate(i) for i in items],
        total=total or 0,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.post("/bulk-approve", response_model=BulkActionResponse)
async def bulk_approve(
    data: BulkIdsRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    auth_header = request.headers.get("Authorization", "")
    updated = 0
    failed = 0
    errors = []

    for req_id in data.ids:
        result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == req_id))
        shift_req = result.scalar_one_or_none()
        if not shift_req:
            failed += 1
            errors.append(f"Request #{req_id}: not found")
            continue

        if not shift_req.employee_id or not shift_req.shift_id:
            failed += 1
            errors.append(f"Request #{req_id}: missing employee_id or shift_id")
            continue

        try:
            await _approve_shift_request(shift_req, auth_header, db)
            await db.commit()
            updated += 1
        except HTTPException as e:
            await db.rollback()
            failed += 1
            errors.append(f"Request #{req_id}: {e.detail}")
        except Exception as e:
            await db.rollback()
            failed += 1
            errors.append(f"Request #{req_id}: {str(e)}")

    return BulkActionResponse(
        success=(failed == 0),
        updated_count=updated,
        failed_count=failed,
        errors=errors,
    )


@router.post("/bulk-reject", response_model=BulkActionResponse)
async def bulk_reject(
    data: BulkIdsRequest,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.cancel_shiftrequest")),
):
    updated = 0
    failed = 0
    errors = []

    for req_id in data.ids:
        result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == req_id))
        shift_req = result.scalar_one_or_none()
        if not shift_req:
            failed += 1
            errors.append(f"Request #{req_id}: not found")
            continue

        try:
            await _reject_shift_request(shift_req, db)
            await db.commit()
            updated += 1
        except Exception as e:
            await db.rollback()
            failed += 1
            errors.append(f"Request #{req_id}: {str(e)}")

    return BulkActionResponse(
        success=(failed == 0),
        updated_count=updated,
        failed_count=failed,
        errors=errors,
    )


@router.post("/bulk-delete", response_model=BulkActionResponse)
async def bulk_delete(
    data: BulkIdsRequest,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.delete_shiftrequest")),
):
    result = await db.execute(
        delete(ShiftRequest).where(ShiftRequest.id.in_(data.ids))
    )
    await db.commit()
    return BulkActionResponse(success=True, updated_count=result.rowcount)


@router.post("/{item_id}/approve", response_model=ShiftRequestRead)
async def approve_shift_request(
    item_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.approve_shiftrequest")),
):
    result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == item_id))
    shift_req = result.scalar_one_or_none()
    if not shift_req:
        raise HTTPException(status_code=404, detail="Shift request not found")

    auth_header = request.headers.get("Authorization", "")
    updated = await _approve_shift_request(shift_req, auth_header, db)
    await db.commit()
    return ShiftRequestRead.model_validate(updated)


@router.post("/{item_id}/reject", response_model=ShiftRequestRead)
async def reject_shift_request(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.cancel_shiftrequest")),
):
    result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == item_id))
    shift_req = result.scalar_one_or_none()
    if not shift_req:
        raise HTTPException(status_code=404, detail="Shift request not found")

    updated = await _reject_shift_request(shift_req, db)
    await db.commit()
    return ShiftRequestRead.model_validate(updated)


@router.get("/{item_id}", response_model=ShiftRequestRead)
async def get_shift_request(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.view_shiftrequest")),
):
    result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == item_id))
    shift_req = result.scalar_one_or_none()
    if not shift_req:
        raise HTTPException(status_code=404, detail="Shift request not found")
    return ShiftRequestRead.model_validate(shift_req)


@router.post("", response_model=ShiftRequestRead, status_code=201)
async def create_shift_request(
    data: ShiftRequestCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("core.add_shiftrequest")),
):
    shift_req = ShiftRequest(**data.model_dump(exclude_unset=True))
    if hasattr(shift_req, "created_by_id"):
        shift_req.created_by_id = user.user_id
    db.add(shift_req)
    await db.flush()
    await db.refresh(shift_req)
    return ShiftRequestRead.model_validate(shift_req)


@router.put("/{item_id}", response_model=ShiftRequestRead)
async def update_shift_request(
    item_id: int,
    data: ShiftRequestUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("core.change_shiftrequest")),
):
    result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == item_id))
    shift_req = result.scalar_one_or_none()
    if not shift_req:
        raise HTTPException(status_code=404, detail="Shift request not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(shift_req, key, value)
    if hasattr(shift_req, "modified_by_id"):
        shift_req.modified_by_id = user.user_id
    await db.flush()
    await db.refresh(shift_req)
    return ShiftRequestRead.model_validate(shift_req)


@router.delete("/{item_id}", status_code=204)
async def delete_shift_request(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.delete_shiftrequest")),
):
    result = await db.execute(select(ShiftRequest).where(ShiftRequest.id == item_id))
    shift_req = result.scalar_one_or_none()
    if not shift_req:
        raise HTTPException(status_code=404, detail="Shift request not found")
    await db.delete(shift_req)
