from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class RotatingWorkTypeBase(BaseModel):
    name: str
    work_type1_id: int
    work_type2_id: int
    additional_data: Optional[Dict[str, Any]] = None

class RotatingWorkTypeCreate(RotatingWorkTypeBase):
    pass

class RotatingWorkTypeUpdate(BaseModel):
    name: Optional[str] = None
    work_type1_id: Optional[int] = None
    work_type2_id: Optional[int] = None
    additional_data: Optional[Dict[str, Any]] = None

class RotatingWorkTypeRead(HorillaSchemaBase, RotatingWorkTypeBase):
    id: int
