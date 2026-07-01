from typing import Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaAuditSchema


class BulkIdsRequest(BaseModel):
    ids: list[int]


class BulkActionResponse(BaseModel):
    success: bool
    updated_count: int
    failed_count: int = 0
    errors: list[str] = []

class RotatingWorkTypeAssignBase(BaseModel):
    employee_id: Optional[int] = None
    rotating_work_type_id: int
    start_date: date
    next_change_date: Optional[date] = None
    current_work_type_id: Optional[int] = None
    next_work_type_id: Optional[int] = None
    based_on: str
    rotate_after_day: int = 7
    rotate_every_weekend: Optional[str] = None
    rotate_every: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class RotatingWorkTypeAssignCreate(RotatingWorkTypeAssignBase):
    pass

class RotatingWorkTypeAssignUpdate(BaseModel):
    employee_id: Optional[int] = None
    rotating_work_type_id: Optional[int] = None
    start_date: Optional[date] = None
    next_change_date: Optional[date] = None
    current_work_type_id: Optional[int] = None
    next_work_type_id: Optional[int] = None
    based_on: Optional[str] = None
    rotate_after_day: Optional[int] = None
    rotate_every_weekend: Optional[str] = None
    rotate_every: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class RotatingWorkTypeAssignRead(HorillaAuditSchema, RotatingWorkTypeAssignBase):
    pass
