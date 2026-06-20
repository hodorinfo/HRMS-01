"""Shared Pydantic schemas."""

from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class HorillaSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HorillaAuditSchema(HorillaSchemaBase):
    id: int
    created_at: Optional[datetime] = None
    created_by_id: Optional[int] = None
    modified_by_id: Optional[int] = None
    is_active: bool = True


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
