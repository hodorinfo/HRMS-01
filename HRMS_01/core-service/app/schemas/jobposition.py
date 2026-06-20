from typing import Optional
from pydantic import BaseModel, ConfigDict

class JobPositionCreate(BaseModel):
    job_position: str
    department_id: int

class JobPositionUpdate(BaseModel):
    job_position: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None

class JobPositionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    job_position: str
    department_id: int
    is_active: bool = True
