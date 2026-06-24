from typing import Optional
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class CompanyLeavesBase(BaseModel):
    based_on_week: str
    based_on_week_day: str

class CompanyLeavesCreate(CompanyLeavesBase):
    pass

class CompanyLeavesUpdate(BaseModel):
    based_on_week: Optional[str] = None
    based_on_week_day: Optional[str] = None

class CompanyLeavesRead(HorillaSchemaBase, CompanyLeavesBase):
    id: int
