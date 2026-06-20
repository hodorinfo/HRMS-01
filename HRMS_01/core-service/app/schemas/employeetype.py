from typing import Optional
from pydantic import BaseModel, ConfigDict

class EmployeeTypeCreate(BaseModel):
    employee_type: str

class EmployeeTypeUpdate(BaseModel):
    employee_type: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_type: str
    is_active: bool = True
