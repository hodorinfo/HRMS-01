from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Legacy recruitment schemas removed

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

class OnboardingStageCreate(BaseModel):
    recruitment_id: int
    sequence: int = 0
    is_final_stage: bool = False

class OnboardingStageRead(HorillaSchema):
    id: int
    recruitment_id: int
    sequence: int
    is_final_stage: bool

class OnboardingTaskCreate(BaseModel):
    stage_id: int

class OnboardingTaskRead(HorillaSchema):
    id: int
    stage_id: int

class CandidateStageCreate(BaseModel):
    candidate_id: int
    onboarding_stage_id: int
    onboarding_end_date: Optional[date] = None
    sequence: int = 0

class CandidateStageRead(HorillaSchema):
    id: int
    candidate_id: int
    onboarding_stage_id: int
    onboarding_end_date: Optional[date] = None
    sequence: int

class CandidateTaskCreate(BaseModel):
    candidate_id: int
    stage_id: int
    onboarding_task_id: int
    status: str = "todo"

class CandidateTaskRead(HorillaSchema):
    id: int
    candidate_id: int
    stage_id: int
    onboarding_task_id: int
    status: str

class OnboardingPortalCreate(BaseModel):
    candidate_id: int
    token: str
    used: bool = False
    count: int = 0

class OnboardingPortalRead(HorillaSchema):
    id: int
    candidate_id: int
    token: str
    used: bool
    count: int

# --- MISSING PMS MODELS ---
class PeriodCreate(BaseModel):
    period_name: str
    start_date: date
    end_date: date

class PeriodRead(HorillaSchema):
    id: int
    period_name: str
    start_date: date
    end_date: date
    is_active: bool = True

class KeyResultCreate(BaseModel):
    title: str
    description: Optional[str] = None
    progress_type: str = "%"
    target_value: int = 0
    duration: int = 0
    company_id: Optional[int] = None

class KeyResultRead(HorillaSchema):
    id: int
    title: str
    progress_type: str
    target_value: int
    duration: int
    archive: bool = False
    is_active: bool = True

# --- MISSING OFFBOARDING MODELS ---
class OffboardingStageCreate(BaseModel):
    title: str
    type: str
    offboarding_id: int
    sequence: int = 0

class OffboardingStageRead(HorillaSchema):
    id: int
    title: str
    type: str
    offboarding_id: int
    sequence: int
    is_active: bool = True

class OffboardingEmployeeCreate(BaseModel):
    employee_id: int
    stage_id: int
    notice_period: int = 0
    unit: str = "day"
    notice_period_starts: Optional[date] = None
    notice_period_ends: Optional[date] = None

class OffboardingEmployeeRead(HorillaSchema):
    id: int
    employee_id: int
    stage_id: int
    notice_period: int
    unit: str
    is_active: bool = True

class OffboardingTaskCreate(BaseModel):
    title: str
    stage_id: int

class OffboardingTaskRead(HorillaSchema):
    id: int
    title: str
    stage_id: int
    is_active: bool = True

class EmployeeTaskCreate(BaseModel):
    employee_id: int
    status: str = "todo"
    task_id: int

class EmployeeTaskRead(HorillaSchema):
    id: int
    employee_id: int
    status: str
    task_id: int
    is_active: bool = True

from .phm_recruitment import (
    PHMHiringRequestCreate, PHMHiringRequestUpdate, PHMHiringRequestRead,
    PHMPositionPrepCreate, PHMPositionPrepUpdate, PHMPositionPrepRead,
    PHMIdealCandidateProfileCreate, PHMIdealCandidateProfileUpdate, PHMIdealCandidateProfileRead,
    PHMInterviewQuestionBankCreate, PHMInterviewQuestionBankUpdate, PHMInterviewQuestionBankRead,
    PHMSourcingChannelCreate, PHMSourcingChannelUpdate, PHMSourcingChannelRead,
    PHMJobDescriptionCreate, PHMJobDescriptionUpdate, PHMJobDescriptionRead,
    PHMPipelineStageCreate, PHMPipelineStageUpdate, PHMPipelineStageRead,
    PHMRejectionReasonCreate, PHMRejectionReasonUpdate, PHMRejectionReasonRead,
    PHMCandidateCreate, PHMCandidateUpdate, PHMCandidateRead,
    PHMCandidateScreeningCreate, PHMCandidateScreeningUpdate, PHMCandidateScreeningRead,
    PHMInterviewFeedbackCreate, PHMInterviewFeedbackUpdate, PHMInterviewFeedbackRead,
    PHMHiringErrorFlagCreate, PHMHiringErrorFlagUpdate, PHMHiringErrorFlagRead,
    PHMHiringMasterTemplateCreate, PHMHiringMasterTemplateUpdate, PHMHiringMasterTemplateRead,
    PHMMasterProcessStepCreate, PHMMasterProcessStepUpdate, PHMMasterProcessStepRead,
    PHMStepDependencyCreate, PHMStepDependencyUpdate, PHMStepDependencyRead,
    PHMRequestStepTrackerCreate, PHMRequestStepTrackerUpdate, PHMRequestStepTrackerRead,
    PHMOfferDetailsCreate, PHMOfferDetailsUpdate, PHMOfferDetailsRead
)
