from typing import Optional
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class AnnouncementBase(BaseModel):
    title: str
    description: Optional[str] = None
    disable_comments: bool = False
    public_comments: bool = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    disable_comments: Optional[bool] = None
    public_comments: Optional[bool] = None

class AnnouncementRead(HorillaSchemaBase, AnnouncementBase):
    id: int
