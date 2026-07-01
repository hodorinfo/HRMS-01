"""Rotating work type assign list and bulk action endpoints."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models import RotatingWorkTypeAssign
from app.schemas.rotatingworktypeassign import (
    BulkActionResponse,
    BulkIdsRequest,
    RotatingWorkTypeAssignCreate,
    RotatingWorkTypeAssignRead,
    RotatingWorkTypeAssignUpdate,
)
from horilla_common.schemas import PaginatedResponse

router = APIRouter(prefix="/rotating-work-type-assigns", tags=["base"])


@router.get("", response_model=PaginatedResponse[RotatingWorkTypeAssignRead])
async def list_assigns(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    employee_id: Optional[int] = None,
    rotating_work_type_id: Optional[int] = None,
    based_on: Optional[str] = None,
    current_work_type_id: Optional[int] = None,
    next_work_type_id: Optional[int] = None,
    next_change_date: Optional[date] = None,
    next_change_date_from: Optional[date] = None,
    next_change_date_to: Optional[date] = None,
    start_date_from: Optional[date] = None,
    start_date_to: Optional[date] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.view_rotatingworktypeassign")),
):
    query = select(RotatingWorkTypeAssign)

    if employee_id is not None:
        query = query.where(RotatingWorkTypeAssign.employee_id == employee_id)
    if rotating_work_type_id is not None:
        query = query.where(RotatingWorkTypeAssign.rotating_work_type_id == rotating_work_type_id)
    if based_on is not None:
        query = query.where(RotatingWorkTypeAssign.based_on.ilike(based_on))
    if current_work_type_id is not None:
        query = query.where(RotatingWorkTypeAssign.current_work_type_id == current_work_type_id)
    if next_work_type_id is not None:
        query = query.where(RotatingWorkTypeAssign.next_work_type_id == next_work_type_id)
    if next_change_date is not None:
        query = query.where(RotatingWorkTypeAssign.next_change_date == next_change_date)
    if next_change_date_from is not None:
        query = query.where(RotatingWorkTypeAssign.next_change_date >= next_change_date_from)
    if next_change_date_to is not None:
        query = query.where(RotatingWorkTypeAssign.next_change_date <= next_change_date_to)
    if start_date_from is not None:
        query = query.where(RotatingWorkTypeAssign.start_date >= start_date_from)
    if start_date_to is not None:
        query = query.where(RotatingWorkTypeAssign.start_date <= start_date_to)
    if is_active is not None:
        query = query.where(RotatingWorkTypeAssign.is_active == is_active)

    total = await db.scalar(
        select(func.count()).select_from(RotatingWorkTypeAssign).where(query.whereclause)
        if query.whereclause is not None
        else select(func.count()).select_from(RotatingWorkTypeAssign)
    )
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        items=[RotatingWorkTypeAssignRead.model_validate(i) for i in items],
        total=total or 0,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.post("/bulk-archive", response_model=BulkActionResponse)
async def bulk_archive(
    data: BulkIdsRequest,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.change_rotatingworktypeassign")),
):
    updated = 0
    failed = 0
    errors = []

    for item_id in data.ids:
        result = await db.execute(
            select(RotatingWorkTypeAssign).where(RotatingWorkTypeAssign.id == item_id)
        )
        assign = result.scalar_one_or_none()
        if not assign:
            failed += 1
            errors.append(f"Rotating work type assign #{item_id}: not found")
            continue

        try:
            assign.is_active = False
            await db.flush()
            await db.commit()
            updated += 1
        except Exception as e:
            await db.rollback()
            failed += 1
            errors.append(f"Rotating work type assign #{item_id}: {str(e)}")

    return BulkActionResponse(
        success=(failed == 0),
        updated_count=updated,
        failed_count=failed,
        errors=errors,
    )


@router.post("/bulk-unarchive", response_model=BulkActionResponse)
async def bulk_unarchive(
    data: BulkIdsRequest,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.change_rotatingworktypeassign")),
):
    updated = 0
    failed = 0
    errors = []

    for item_id in data.ids:
        result = await db.execute(
            select(RotatingWorkTypeAssign).where(RotatingWorkTypeAssign.id == item_id)
        )
        assign = result.scalar_one_or_none()
        if not assign:
            failed += 1
            errors.append(f"Rotating work type assign #{item_id}: not found")
            continue

        try:
            assign.is_active = True
            await db.flush()
            await db.commit()
            updated += 1
        except Exception as e:
            await db.rollback()
            failed += 1
            errors.append(f"Rotating work type assign #{item_id}: {str(e)}")

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
    _perm=Depends(require_permission("core.delete_rotatingworktypeassign")),
):
    result = await db.execute(
        delete(RotatingWorkTypeAssign).where(RotatingWorkTypeAssign.id.in_(data.ids))
    )
    await db.commit()
    return BulkActionResponse(success=True, updated_count=result.rowcount)


@router.get("/{item_id}", response_model=RotatingWorkTypeAssignRead)
async def get_assign(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.view_rotatingworktypeassign")),
):
    result = await db.execute(
        select(RotatingWorkTypeAssign).where(RotatingWorkTypeAssign.id == item_id)
    )
    assign = result.scalar_one_or_none()
    if not assign:
        raise HTTPException(status_code=404, detail="Rotating work type assign not found")
    return RotatingWorkTypeAssignRead.model_validate(assign)


@router.post("", response_model=RotatingWorkTypeAssignRead, status_code=201)
async def create_assign(
    data: RotatingWorkTypeAssignCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("core.add_rotatingworktypeassign")),
):
    assign = RotatingWorkTypeAssign(**data.model_dump(exclude_unset=True))
    if hasattr(assign, "created_by_id"):
        assign.created_by_id = user.user_id
    db.add(assign)
    await db.flush()
    await db.refresh(assign)
    return RotatingWorkTypeAssignRead.model_validate(assign)


@router.put("/{item_id}", response_model=RotatingWorkTypeAssignRead)
async def update_assign(
    item_id: int,
    data: RotatingWorkTypeAssignUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("core.change_rotatingworktypeassign")),
):
    result = await db.execute(
        select(RotatingWorkTypeAssign).where(RotatingWorkTypeAssign.id == item_id)
    )
    assign = result.scalar_one_or_none()
    if not assign:
        raise HTTPException(status_code=404, detail="Rotating work type assign not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(assign, key, value)
    if hasattr(assign, "modified_by_id"):
        assign.modified_by_id = user.user_id
    await db.flush()
    await db.refresh(assign)
    return RotatingWorkTypeAssignRead.model_validate(assign)


@router.delete("/{item_id}", status_code=204)
async def delete_assign(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("core.delete_rotatingworktypeassign")),
):
    result = await db.execute(
        select(RotatingWorkTypeAssign).where(RotatingWorkTypeAssign.id == item_id)
    )
    assign = result.scalar_one_or_none()
    if not assign:
        raise HTTPException(status_code=404, detail="Rotating work type assign not found")
    await db.delete(assign)
