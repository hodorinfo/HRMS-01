from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class RotatingShiftBase(BaseModel):
    name: str
    shift1_id: int
    shift2_id: int
    additional_data: Optional[Dict[str, Any]] = None

class RotatingShiftCreate(RotatingShiftBase):
    pass

class RotatingShiftUpdate(BaseModel):
    name: Optional[str] = None
    shift1_id: Optional[int] = None
    shift2_id: Optional[int] = None
    additional_data: Optional[Dict[str, Any]] = None

class RotatingShiftRead(HorillaSchemaBase, RotatingShiftBase):
    id: int
