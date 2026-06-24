from typing import Optional
from pydantic import BaseModel, ConfigDict

class AnnouncementViewBase(BaseModel):
    announcement_id: int
    employee_id: int
    viewed: bool = False

class AnnouncementViewCreate(AnnouncementViewBase):
    pass

class AnnouncementViewUpdate(BaseModel):
    viewed: Optional[bool] = None
    is_active: Optional[bool] = None

class AnnouncementViewRead(AnnouncementViewBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool = True
