from typing import Optional
from pydantic import BaseModel, ConfigDict

class JobRoleCreate(BaseModel):
    job_position_id: int
    job_role: Optional[str] = None

class JobRoleUpdate(BaseModel):
    job_position_id: Optional[int] = None
    job_role: Optional[str] = None
    is_active: Optional[bool] = None

class JobRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    job_position_id: int
    job_role: Optional[str] = None
    is_active: bool = True
