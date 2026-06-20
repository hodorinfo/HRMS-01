"""Generic CRUD router factory."""

from typing import Any, Callable, Generic, Optional, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

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
) -> APIRouter:
    router = APIRouter(prefix=prefix)

    @router.get("", response_model=PaginatedResponse[read_schema])
    async def list_items(
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=200),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        offset = (page - 1) * page_size
        total = await db.scalar(select(func.count()).select_from(model))
        result = await db.execute(select(model).offset(offset).limit(page_size))
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
    ):
        item = model(**data.model_dump(exclude_unset=True))
        if hasattr(item, "created_by_id"):
            item.created_by_id = user.user_id
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return read_schema.model_validate(item)

    @router.put("/{item_id}", response_model=read_schema)
    async def update_item(
        item_id: int,
        data: update_schema,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
    ):
        result = await db.execute(select(model).where(getattr(model, id_field) == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        if hasattr(item, "modified_by_id"):
            item.modified_by_id = user.user_id
        await db.flush()
        await db.refresh(item)
        return read_schema.model_validate(item)

    @router.delete("/{item_id}", status_code=204)
    async def delete_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await db.execute(select(model).where(getattr(model, id_field) == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        await db.delete(item)

    return router
