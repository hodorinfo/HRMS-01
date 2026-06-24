from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class WorkTypeRequestCreate(BaseModel):
    employee_id: Optional[int] = None
    work_type_id: int
    previous_work_type_id: Optional[int] = None
    requested_date: Optional[date] = None
    requested_till: Optional[date] = None
    description: Optional[str] = None
    is_permanent_work_type: bool = False
    approved: bool = False
    canceled: bool = False
    work_type_changed: bool = False

class WorkTypeRequestUpdate(BaseModel):
    approved: Optional[bool] = None
    canceled: Optional[bool] = None
    work_type_changed: Optional[bool] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class WorkTypeRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: Optional[int] = None
    work_type_id: int
    approved: bool = False
    canceled: bool = False
    work_type_changed: bool = False
    previous_work_type_id: Optional[int] = None
    requested_date: Optional[date] = None
    requested_till: Optional[date] = None
    description: Optional[str] = None
    is_permanent_work_type: bool = False
    is_active: bool = True
