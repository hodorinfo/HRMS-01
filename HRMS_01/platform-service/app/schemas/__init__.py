from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class MailAutomationCreate(BaseModel):
    title: str
    model: str
    mail_to: str
    trigger: str
    delivery_channel: str = "email"

class MailAutomationRead(HorillaSchema):
    id: int
    title: str
    model: str
    trigger: str
    is_active: bool = True

class NotificationCreate(BaseModel):
    recipient_id: int
    verb: str
    description: Optional[str] = None
    level: str = "info"

class NotificationRead(HorillaSchema):
    id: int
    recipient_id: int
    verb: str
    unread: bool = True
    timestamp: datetime
    level: str

class DocumentRequestCreate(BaseModel):
    title: str
    format: str = "any"
    max_size: int = 5
    description: Optional[str] = None

class DocumentRequestRead(HorillaSchema):
    id: int
    title: str
    format: str
    max_size: int = 5
    description: Optional[str] = None
    is_active: bool = True

class DocumentCreate(BaseModel):
    title: str
    employee_id: int
    document_request_id: Optional[int] = None
    document: Optional[str] = None
    status: str = "requested"
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    notify_before: int = 1
    is_digital_asset: bool = False

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    document_request_id: Optional[int] = None
    document: Optional[str] = None
    status: Optional[str] = None
    reject_reason: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    notify_before: Optional[int] = None
    is_digital_asset: Optional[bool] = None

class DocumentRead(HorillaSchema):
    id: int
    title: str
    employee_id: int
    document_request_id: Optional[int] = None
    document: Optional[str] = None
    status: str
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    notify_before: int = 1
    is_digital_asset: bool = False
    is_active: bool = True
