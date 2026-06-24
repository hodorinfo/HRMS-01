from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ShiftRequestCreate(BaseModel):
    employee_id: Optional[int] = None
    shift_id: int
    previous_shift_id: Optional[int] = None
    requested_date: Optional[date] = None
    requested_till: Optional[date] = None
    description: Optional[str] = None
    is_permanent_shift: bool = False
    approved: bool = False
    canceled: bool = False
    shift_changed: bool = False

class ShiftRequestUpdate(BaseModel):
    approved: Optional[bool] = None
    canceled: Optional[bool] = None
    shift_changed: Optional[bool] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ShiftRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: Optional[int] = None
    shift_id: int
    approved: bool = False
    canceled: bool = False
    shift_changed: bool = False
    previous_shift_id: Optional[int] = None
    requested_date: Optional[date] = None
    requested_till: Optional[date] = None
    description: Optional[str] = None
    is_permanent_shift: bool = False
    is_active: bool = True
