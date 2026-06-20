from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class HolidaysCreate(BaseModel):
    name: str
    start_date: date
    end_date: Optional[date] = None
    recurring: bool = False
    company_id: Optional[int] = None

class HolidaysUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    recurring: Optional[bool] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = None

class HolidaysRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    start_date: date
    end_date: Optional[date] = None
    recurring: bool = False
    company_id: Optional[int] = None
    is_active: bool = True
