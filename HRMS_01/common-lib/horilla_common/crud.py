"""Generic CRUD router factory."""

from typing import Any, Callable, Generic, Optional, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from horilla_common.schemas import PaginatedResponse

ModelT = TypeVar("ModelT")
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
ReadSchemaT = TypeVar("ReadSchemaT", bound=BaseModel)


def create_crud_router(
    prefix: str,
    model: Type[ModelT],
    create_schema: Type[CreateSchemaT],
    update_schema: Type[UpdateSchemaT],
    read_schema: Type[ReadSchemaT],
    get_db: Callable,
    get_current_user: Callable,
    module: str,
    id_field: str = "id",
    get_permission_dep: Optional[Callable[[str], Callable]] = None,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[module])

    _view_perm = Depends(get_permission_dep("view")) if get_permission_dep else Depends(get_current_user)
    _add_perm = Depends(get_permission_dep("add")) if get_permission_dep else Depends(get_current_user)
    _change_perm = Depends(get_permission_dep("change")) if get_permission_dep else Depends(get_current_user)
    _delete_perm = Depends(get_permission_dep("delete")) if get_permission_dep else Depends(get_current_user)

    @router.get("", response_model=PaginatedResponse[read_schema])
    async def list_items(
        request: Request,
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=200),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
        _perm=_view_perm,
    ):
        offset = (page - 1) * page_size

        from sqlalchemy import or_, String, cast, Date
        base_query = select(model)

        SKIP_KEYS = {"page", "page_size", "group_by", "ordering"}

        for key, value in request.query_params.items():
            if key in SKIP_KEYS or not value:
                continue

            # --- Django-style lookup operators ---
            if "__" in key:
                field_name, operator = key.rsplit("__", 1)
                if hasattr(model, field_name):
                    column = getattr(model, field_name)
                    col_type = type(column.type).__name__
                    try:
                        if operator == "gte":
                            base_query = base_query.where(column >= value)
                        elif operator == "lte":
                            base_query = base_query.where(column <= value)
                        elif operator == "icontains":
                            base_query = base_query.where(cast(column, String).ilike(f"%{value}%"))
                        elif operator == "in":
                            ids = [v.strip() for v in value.split(",") if v.strip()]
                            if col_type in ["Integer", "BigInteger", "SmallInteger"]:
                                ids = [int(i) for i in ids if i.isdigit()]
                            base_query = base_query.where(column.in_(ids))
                        elif operator == "isnull":
                            if value.lower() == "true":
                                base_query = base_query.where(column.is_(None))
                            else:
                                base_query = base_query.where(column.isnot(None))
                    except Exception:
                        pass  # Skip malformed filter
                continue

            # --- Exact match on model columns ---
            if hasattr(model, key):
                column = getattr(model, key)
                col_type_name = type(column.type).__name__
                try:
                    if col_type_name == "Boolean" or value.lower() in ["true", "false"]:
                        base_query = base_query.where(column == (value.lower() == "true"))
                    elif col_type_name in ["Integer", "BigInteger", "SmallInteger"]:
                        if value.lstrip("-").isdigit():
                            base_query = base_query.where(column == int(value))
                    elif col_type_name in ["String", "Text", "VARCHAR", "Enum"]:
                        base_query = base_query.where(func.lower(cast(column, String)) == value.lower())
                    else:
                        base_query = base_query.where(cast(column, String) == value)
                except Exception:
                    pass
                continue

            # --- Generic search ---
            if key == "search" and value.strip():
                text_columns = [
                    getattr(model, c.name) for c in model.__table__.columns
                    if type(c.type).__name__ in ["String", "Text", "VARCHAR"]
                ]
                if text_columns:
                    base_query = base_query.where(or_(*[c.ilike(f"%{value}%") for c in text_columns]))

        total = await db.scalar(select(func.count()).select_from(base_query.subquery()))
        result = await db.execute(base_query.offset(offset).limit(page_size))
        items = result.scalars().all()
        pages = (total + page_size - 1) // page_size if total else 0
        return PaginatedResponse(
            items=[read_schema.model_validate(i) for i in items],
            total=total or 0,
            page=page,
            page_size=page_size,
            pages=pages,
        )

    @router.get("/{item_id}", response_model=read_schema)
    async def get_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
        _perm=_view_perm,
    ):
        result = await db.execute(select(model).where(getattr(model, id_field) == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        return read_schema.model_validate(item)

    @router.post("", response_model=read_schema, status_code=201)
    async def create_item(
        data: create_schema,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
        _perm=_add_perm,
    ):
        item = model(**data.model_dump(exclude_unset=True))
        if hasattr(item, "created_by_id"):
            item.created_by_id = user.user_id
        db.add(item)
        try:
            await db.flush()
            await db.refresh(item)
        except IntegrityError as e:
            await db.rollback()
            error_msg = str(e.orig) if e.orig else str(e)
            user_friendly_msg = error_msg
            if "DETAIL:" in error_msg:
                detail_part = error_msg.split("DETAIL:")[1].strip()
                if "foreign key constraint" in error_msg.lower():
                    user_friendly_msg = f"Missing Reference Error: {detail_part}"
                elif "unique constraint" in error_msg.lower() or "duplicate key" in error_msg.lower():
                    user_friendly_msg = f"Duplicate Error: {detail_part}"
                else:
                    user_friendly_msg = f"Database Error: {detail_part}"
            else:
                user_friendly_msg = f"Database Integrity Error: {error_msg.split(chr(10))[0]}"
            raise HTTPException(status_code=400, detail=user_friendly_msg)
        return read_schema.model_validate(item)

    @router.put("/{item_id}", response_model=read_schema)
    async def update_item(
        item_id: int,
        data: update_schema,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
        _perm=_change_perm,
    ):
        result = await db.execute(select(model).where(getattr(model, id_field) == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        if hasattr(item, "modified_by_id"):
            item.modified_by_id = user.user_id
        try:
            await db.flush()
            await db.refresh(item)
        except IntegrityError as e:
            await db.rollback()
            error_msg = str(e.orig) if e.orig else str(e)
            user_friendly_msg = error_msg
            if "DETAIL:" in error_msg:
                detail_part = error_msg.split("DETAIL:")[1].strip()
                if "foreign key constraint" in error_msg.lower():
                    user_friendly_msg = f"Missing Reference Error: {detail_part}"
                elif "unique constraint" in error_msg.lower() or "duplicate key" in error_msg.lower():
                    user_friendly_msg = f"Duplicate Error: {detail_part}"
                else:
                    user_friendly_msg = f"Database Error: {detail_part}"
            else:
                user_friendly_msg = f"Database Integrity Error: {error_msg.split(chr(10))[0]}"
            raise HTTPException(status_code=400, detail=user_friendly_msg)
        return read_schema.model_validate(item)

    @router.delete("/{item_id}", status_code=204)
    async def delete_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
        _perm=_delete_perm,
    ):
        result = await db.execute(select(model).where(getattr(model, id_field) == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        await db.delete(item)

    return router
