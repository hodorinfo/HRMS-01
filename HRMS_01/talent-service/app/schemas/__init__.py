from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class RecruitmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    job_position_id: Optional[int] = None
    vacancy: int = 0
    company_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class RecruitmentUpdate(BaseModel):
    title: Optional[str] = None
    closed: Optional[bool] = None
    is_published: Optional[bool] = None

class RecruitmentRead(HorillaSchema):
    id: int
    title: str
    vacancy: int
    closed: bool = False
    is_published: bool = False
    is_active: bool = True

class CandidateCreate(BaseModel):
    name: str
    recruitment_id: int
    email: EmailStr
    job_position_id: Optional[int] = None
    stage_id: Optional[int] = None
    mobile: Optional[str] = None
    source: str = "application"

class CandidateUpdate(BaseModel):
    stage_id: Optional[int] = None
    hired: Optional[bool] = None
    converted: Optional[bool] = None
    offer_letter_status: Optional[str] = None

class CandidateRead(HorillaSchema):
    id: int
    name: str
    recruitment_id: int
    email: str
    stage_id: Optional[int] = None
    hired: bool = False
    converted: bool = False
    is_active: bool = True

class ObjectiveCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration_unit: str = "days"
    duration: int = 0
    company_id: Optional[int] = None

class ObjectiveRead(HorillaSchema):
    id: int
    title: str
    duration: int
    archive: bool = False
    is_active: bool = True

class EmployeeObjectiveCreate(BaseModel):
    objective: str
    objective_id: int
    employee_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class EmployeeObjectiveRead(HorillaSchema):
    id: int
    objective: str
    employee_id: int
    status: str
    progress_percentage: int = 0
    is_active: bool = True

class FeedbackCreate(BaseModel):
    review_cycle: str
    manager_id: int
    employee_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class FeedbackRead(HorillaSchema):
    id: int
    review_cycle: str
    manager_id: int
    employee_id: int
    status: str
    is_active: bool = True

class OffboardingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    company_id: Optional[int] = None

class OffboardingRead(HorillaSchema):
    id: int
    title: str
    status: str
    is_active: bool = True

class ResignationLetterCreate(BaseModel):
    employee_id: int
    title: str
    description: Optional[str] = None
    planned_to_leave_on: date

class ResignationLetterRead(HorillaSchema):
    id: int
    employee_id: int
    title: str
    planned_to_leave_on: date
    status: str
    is_active: bool = True
