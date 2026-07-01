from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ShiftRequestCommentCreate(BaseModel):
    request_id: int
    comment: Optional[str] = None


class ShiftRequestCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    request_id: int
    employee_id: int
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    is_active: bool = True
