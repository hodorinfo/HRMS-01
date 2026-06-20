from typing import Optional
from pydantic import BaseModel, ConfigDict

class MultipleApprovalConditionCreate(BaseModel):
    department_id: int
    condition_field: str
    condition_operator: str
    condition_value: Optional[str] = None
    condition_start_value: Optional[str] = None
    condition_end_value: Optional[str] = None
    company_id: Optional[int] = None

class MultipleApprovalConditionUpdate(BaseModel):
    condition_field: Optional[str] = None
    condition_operator: Optional[str] = None
    condition_value: Optional[str] = None
    condition_start_value: Optional[str] = None
    condition_end_value: Optional[str] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = None

class MultipleApprovalConditionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    department_id: int
    condition_field: str
    condition_operator: str
    condition_value: Optional[str] = None
    company_id: Optional[int] = None
    is_active: bool = True
