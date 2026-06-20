from typing import Optional
from pydantic import BaseModel, ConfigDict

class WorkTypeCreate(BaseModel):
    work_type: str

class WorkTypeUpdate(BaseModel):
    work_type: Optional[str] = None
    is_active: Optional[bool] = None

class WorkTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    work_type: str
    is_active: bool = True
