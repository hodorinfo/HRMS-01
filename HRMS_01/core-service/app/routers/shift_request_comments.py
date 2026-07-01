"""Shift request comment CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models import ShiftRequestComment
from app.schemas.shiftrequestcomment import (
    ShiftRequestCommentCreate,
    ShiftRequestCommentRead,
)
from horilla_common.jwt import TokenPayload

router = APIRouter(prefix="/shift-request-comments", tags=["base"])


@router.get("", response_model=list[ShiftRequestCommentRead])
async def list_comments(
    request_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    _user: TokenPayload = Depends(get_current_user),
    _perm=Depends(require_permission("core.view_shiftrequestcomment")),
):
    result = await db.execute(
        select(ShiftRequestComment)
        .where(ShiftRequestComment.request_id == request_id)
        .where(ShiftRequestComment.is_active == True)
        .order_by(ShiftRequestComment.created_at)
    )
    return [
        ShiftRequestCommentRead.model_validate(c) for c in result.scalars().all()
    ]


@router.post("", response_model=ShiftRequestCommentRead, status_code=201)
async def create_comment(
    data: ShiftRequestCommentCreate,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
    _perm=Depends(require_permission("core.add_shiftrequestcomment")),
):
    if not user.employee_id:
        raise HTTPException(
            status_code=400,
            detail="Current user has no linked employee record",
        )
    comment = ShiftRequestComment(
        request_id=data.request_id,
        employee_id=user.employee_id,
        comment=data.comment,
    )
    db.add(comment)
    await db.flush()
    await db.refresh(comment)
    return ShiftRequestCommentRead.model_validate(comment)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
    _perm=Depends(require_permission("core.delete_shiftrequestcomment")),
):
    result = await db.execute(
        select(ShiftRequestComment).where(ShiftRequestComment.id == comment_id)
    )
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.employee_id != user.employee_id and not user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )
    await db.delete(comment)
