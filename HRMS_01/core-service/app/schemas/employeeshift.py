from typing import Optional
from pydantic import BaseModel, ConfigDict

class EmployeeShiftCreate(BaseModel):
    employee_shift: str
    weekly_full_time: Optional[str] = "40:00"
    full_time: str = "200:00"
    grace_time_id: Optional[int] = None

class EmployeeShiftUpdate(BaseModel):
    employee_shift: Optional[str] = None
    weekly_full_time: Optional[str] = None
    full_time: Optional[str] = None
    grace_time_id: Optional[int] = None
    is_active: Optional[bool] = None

class EmployeeShiftRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_shift: str
    weekly_full_time: Optional[str] = None
    full_time: str
    grace_time_id: Optional[int] = None
    is_active: bool = True
