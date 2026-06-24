from typing import Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class RotatingShiftAssignBase(BaseModel):
    employee_id: Optional[int] = None
    rotating_shift_id: int
    start_date: date
    next_change_date: Optional[date] = None
    current_shift_id: Optional[int] = None
    next_shift_id: Optional[int] = None
    based_on: str
    rotate_after_day: int = 7
    rotate_every_weekend: Optional[str] = None
    rotate_every: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class RotatingShiftAssignCreate(RotatingShiftAssignBase):
    pass

class RotatingShiftAssignUpdate(BaseModel):
    employee_id: Optional[int] = None
    rotating_shift_id: Optional[int] = None
    start_date: Optional[date] = None
    next_change_date: Optional[date] = None
    current_shift_id: Optional[int] = None
    next_shift_id: Optional[int] = None
    based_on: Optional[str] = None
    rotate_after_day: Optional[int] = None
    rotate_every_weekend: Optional[str] = None
    rotate_every: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class RotatingShiftAssignRead(HorillaSchemaBase, RotatingShiftAssignBase):
    id: int
