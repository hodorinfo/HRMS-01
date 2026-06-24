from typing import Optional
from pydantic import BaseModel, ConfigDict

class MultipleApprovalManagersBase(BaseModel):
    condition_id: int
    sequence: int
    employee_id: Optional[int] = None
    reporting_manager: Optional[str] = None

class MultipleApprovalManagersCreate(MultipleApprovalManagersBase):
    pass

class MultipleApprovalManagersUpdate(BaseModel):
    condition_id: Optional[int] = None
    sequence: Optional[int] = None
    employee_id: Optional[int] = None
    reporting_manager: Optional[str] = None

class MultipleApprovalManagersRead(MultipleApprovalManagersBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
