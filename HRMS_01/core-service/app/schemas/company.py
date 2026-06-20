from typing import Optional
from pydantic import BaseModel, ConfigDict

class CompanyCreate(BaseModel):
    company: str
    hq: bool = False
    address: str
    country: str
    state: str
    city: str
    zip: str
    icon: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None

class CompanyUpdate(BaseModel):
    company: Optional[str] = None
    hq: Optional[bool] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    icon: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    is_active: Optional[bool] = None

class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company: str
    hq: bool = False
    address: str
    country: str
    state: str
    city: str
    zip: str
    icon: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    is_active: bool = True
