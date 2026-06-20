from typing import Optional
from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    department: str

class DepartmentUpdate(BaseModel):
    department: Optional[str] = None
    is_active: Optional[bool] = None

class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    department: str
    is_active: bool = True
