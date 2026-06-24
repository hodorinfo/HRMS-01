from typing import Optional
from pydantic import BaseModel, ConfigDict

class EmployeeShiftDayBase(BaseModel):
    day: str

class EmployeeShiftDayCreate(EmployeeShiftDayBase):
    pass

class EmployeeShiftDayUpdate(BaseModel):
    day: Optional[str] = None

class EmployeeShiftDayRead(EmployeeShiftDayBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
