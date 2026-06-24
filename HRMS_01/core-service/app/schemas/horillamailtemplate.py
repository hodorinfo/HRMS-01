from typing import Optional
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class HorillaMailTemplateBase(BaseModel):
    title: str
    body: str

class HorillaMailTemplateCreate(HorillaMailTemplateBase):
    pass

class HorillaMailTemplateUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None

class HorillaMailTemplateRead(HorillaSchemaBase, HorillaMailTemplateBase):
    id: int
