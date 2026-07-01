"""Disciplinary actions endpoints."""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from horilla_common.crud import create_crud_router
from horilla_common.schemas import PaginatedResponse
from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models import Actiontype, DisciplinaryAction, DisciplinaryActionEmployee
from app.schemas import (
    ActiontypeCreate, ActiontypeRead, ActiontypeUpdate,
    DisciplinaryActionCreate, DisciplinaryActionRead, DisciplinaryActionUpdate,
    DisciplinaryBulkIdsRequest, DisciplinaryBulkActionResponse,
)

router = APIRouter()
router.include_router(create_crud_router(
    "/action-types", Actiontype,
    ActiontypeCreate, ActiontypeUpdate, ActiontypeRead,
    get_db, get_current_user, "employees",
    get_permission_dep=lambda action: require_permission(f"identity.{action}_actiontype"),
))


def _build_read(action: DisciplinaryAction) -> dict:
    employee_ids = [a.employee_id for a in action.employee_assignments]
    return {
        "id": action.id,
        "employee_ids": employee_ids,
        "action_id": action.action_id,
        "description": action.description,
        "unit_in": action.unit_in,
        "days": action.days,
        "hours": action.hours,
        "start_date": action.start_date,
        "attachment": action.attachment,
        "is_active": action.is_active,
        "created_at": action.created_at,
    }


@router.get("/disciplinary-actions", response_model=PaginatedResponse[DisciplinaryActionRead])
async def list_disciplinary_actions(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None),
    employee_id: Optional[int] = Query(None),
    action_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    start_date_from: Optional[date] = Query(None),
    start_date_to: Optional[date] = Query(None),
    unit_in: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db=Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.view_disciplinaryaction")),
):
    conditions = []
    if search:
        conditions.append(DisciplinaryAction.description.ilike(f"%{search}%"))
    if employee_id:
        subq = select(DisciplinaryActionEmployee.disciplinary_action_id).where(
            DisciplinaryActionEmployee.employee_id == employee_id
        )
        conditions.append(DisciplinaryAction.id.in_(subq))
    if action_id:
        conditions.append(DisciplinaryAction.action_id == action_id)
    if start_date:
        conditions.append(DisciplinaryAction.start_date == start_date)
    if start_date_from:
        conditions.append(DisciplinaryAction.start_date >= start_date_from)
    if start_date_to:
        conditions.append(DisciplinaryAction.start_date <= start_date_to)
    if unit_in:
        conditions.append(DisciplinaryAction.unit_in == unit_in)
    if is_active is not None:
        conditions.append(DisciplinaryAction.is_active == is_active)

    base = select(DisciplinaryAction).options(
        selectinload(DisciplinaryAction.employee_assignments)
    )
    if conditions:
        base = base.where(*conditions)

    offset = (page - 1) * page_size

    count_query = select(func.count()).select_from(DisciplinaryAction)
    if conditions:
        count_query = count_query.where(*conditions)
    total = await db.scalar(count_query)

    result = await db.execute(base.offset(offset).limit(page_size))
    actions = result.scalars().all()
    pages = (total + page_size - 1) // page_size if total else 0
    items = [DisciplinaryActionRead(**_build_read(a)) for a in actions]
    return PaginatedResponse(
        items=items,
        total=total or 0,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/disciplinary-actions/{item_id}", response_model=DisciplinaryActionRead)
async def get_disciplinary_action(
    item_id: int,
    db=Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.view_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .where(DisciplinaryAction.id == item_id)
    )
    action = result.scalar_one_or_none()
    if not action:
        raise HTTPException(status_code=404, detail="Not found")
    return DisciplinaryActionRead(**_build_read(action))


@router.post("/disciplinary-actions", response_model=DisciplinaryActionRead, status_code=201)
async def create_disciplinary_action(
    data: DisciplinaryActionCreate,
    db=Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.add_disciplinaryaction")),
):
    action = DisciplinaryAction(
        employee_id=None,
        action_id=data.action_id,
        description=data.description,
        unit_in=data.unit_in,
        days=data.days,
        hours=data.hours,
        start_date=data.start_date,
        attachment=data.attachment,
        created_by_id=user.user_id,
    )
    db.add(action)
    await db.flush()
    await db.refresh(action)

    for emp_id in data.employee_ids:
        db.add(DisciplinaryActionEmployee(
            disciplinary_action_id=action.id,
            employee_id=emp_id,
        ))
    await db.flush()

    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .where(DisciplinaryAction.id == action.id)
    )
    action = result.scalar_one()
    return DisciplinaryActionRead(**_build_read(action))


@router.put("/disciplinary-actions/{item_id}", response_model=DisciplinaryActionRead)
async def update_disciplinary_action(
    item_id: int,
    data: DisciplinaryActionUpdate,
    db=Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.change_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .where(DisciplinaryAction.id == item_id)
    )
    action = result.scalar_one_or_none()
    if not action:
        raise HTTPException(status_code=404, detail="Not found")

    update_fields = data.model_dump(exclude_unset=True, exclude={"employee_ids"})
    for key, value in update_fields.items():
        setattr(action, key, value)
    action.modified_by_id = user.user_id

    if data.employee_ids is not None:
        existing = await db.execute(
            select(DisciplinaryActionEmployee)
            .where(DisciplinaryActionEmployee.disciplinary_action_id == item_id)
        )
        for row in existing.scalars().all():
            await db.delete(row)
        for emp_id in data.employee_ids:
            db.add(DisciplinaryActionEmployee(
                disciplinary_action_id=item_id,
                employee_id=emp_id,
            ))

    await db.flush()
    await db.refresh(action)

    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .where(DisciplinaryAction.id == item_id)
    )
    action = result.scalar_one()
    return DisciplinaryActionRead(**_build_read(action))


@router.delete("/disciplinary-actions/{item_id}", status_code=204)
async def delete_disciplinary_action(
    item_id: int,
    db=Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.delete_disciplinaryaction")),
):
    result = await db.execute(select(DisciplinaryAction).where(DisciplinaryAction.id == item_id))
    action = result.scalar_one_or_none()
    if not action:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(action)


@router.post(
    "/disciplinary-actions/{item_id}/duplicate",
    response_model=DisciplinaryActionRead,
    status_code=201,
)
async def duplicate_disciplinary_action(
    item_id: int,
    db=Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.add_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .where(DisciplinaryAction.id == item_id)
    )
    original = result.scalar_one_or_none()
    if not original:
        raise HTTPException(status_code=404, detail="Not found")

    new_action = DisciplinaryAction(
        employee_id=None,
        action_id=original.action_id,
        description=original.description,
        unit_in=original.unit_in,
        days=original.days,
        hours=original.hours,
        start_date=original.start_date,
        attachment=original.attachment,
        created_by_id=user.user_id,
    )
    db.add(new_action)
    await db.flush()
    await db.refresh(new_action)

    for a in original.employee_assignments:
        db.add(DisciplinaryActionEmployee(
            disciplinary_action_id=new_action.id,
            employee_id=a.employee_id,
        ))
    await db.flush()

    result = await db.execute(
        select(DisciplinaryAction)
        .options(selectinload(DisciplinaryAction.employee_assignments))
        .where(DisciplinaryAction.id == new_action.id)
    )
    new_action = result.scalar_one()
    return DisciplinaryActionRead(**_build_read(new_action))


@router.post("/disciplinary-actions/bulk-archive", response_model=DisciplinaryBulkActionResponse)
async def bulk_archive_disciplinary_actions(
    data: DisciplinaryBulkIdsRequest,
    db=Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.change_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction).where(
            DisciplinaryAction.id.in_(data.ids),
            DisciplinaryAction.is_active == True,
        )
    )
    actions = result.scalars().all()
    updated = 0
    failed = 0
    for a in actions:
        try:
            a.is_active = False
            a.modified_by_id = user.user_id
            updated += 1
        except Exception:
            failed += 1
    await db.flush()
    return DisciplinaryBulkActionResponse(updated_count=updated, failed_count=failed)


@router.post("/disciplinary-actions/bulk-unarchive", response_model=DisciplinaryBulkActionResponse)
async def bulk_unarchive_disciplinary_actions(
    data: DisciplinaryBulkIdsRequest,
    db=Depends(get_db),
    user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.change_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction).where(
            DisciplinaryAction.id.in_(data.ids),
            DisciplinaryAction.is_active == False,
        )
    )
    actions = result.scalars().all()
    updated = 0
    failed = 0
    for a in actions:
        try:
            a.is_active = True
            a.modified_by_id = user.user_id
            updated += 1
        except Exception:
            failed += 1
    await db.flush()
    return DisciplinaryBulkActionResponse(updated_count=updated, failed_count=failed)


@router.post("/disciplinary-actions/bulk-delete", response_model=DisciplinaryBulkActionResponse)
async def bulk_delete_disciplinary_actions(
    data: DisciplinaryBulkIdsRequest,
    db=Depends(get_db),
    _user=Depends(get_current_user),
    _perm=Depends(require_permission("identity.delete_disciplinaryaction")),
):
    result = await db.execute(
        select(DisciplinaryAction).where(DisciplinaryAction.id.in_(data.ids))
    )
    actions = result.scalars().all()
    ids_found = {a.id for a in actions}
    for a in actions:
        await db.delete(a)
    updated = len(ids_found)
    failed = len(data.ids) - updated
    await db.flush()
    return DisciplinaryBulkActionResponse(updated_count=updated, failed_count=failed)
