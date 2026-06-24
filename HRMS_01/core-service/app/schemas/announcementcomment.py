from typing import Optional
from pydantic import BaseModel, ConfigDict

class AnnouncementCommentBase(BaseModel):
    announcement_id: int
    employee_id: int
    comment: Optional[str] = None

class AnnouncementCommentCreate(AnnouncementCommentBase):
    pass

class AnnouncementCommentUpdate(BaseModel):
    comment: Optional[str] = None
    is_active: Optional[bool] = None

class AnnouncementCommentRead(AnnouncementCommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool = True
