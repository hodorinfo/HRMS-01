from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.phm_recruitment import (
    TriggerEnum, StrategyEnum, PriorityEnum, HiringRequestStatus, PositionTypeEnum,
    SkillTypeEnum, ChannelTypeEnum, CVTypeEnum, RoundNameEnum, ErrorTypeEnum,
    ResponsibleRoleEnum, TrackerStatusEnum, OfferStatusEnum
)

# PHASE 1
class PHMHiringRequestBase(BaseModel):
    title: str
    trigger: TriggerEnum
    strategy: StrategyEnum
    priority: PriorityEnum
    roi_expensive_hire_cost: float = 0.0
    roi_cheap_hire_cost: float = 0.0
    roi_expected_return: float = 0.0
    target_hire_date: Optional[date] = None
    actual_filled_date: Optional[date] = None
    status: HiringRequestStatus = HiringRequestStatus.PENDING

class PHMHiringRequestCreate(PHMHiringRequestBase):
    pass

class PHMHiringRequestUpdate(PHMHiringRequestBase):
    title: Optional[str] = None
    trigger: Optional[TriggerEnum] = None
    strategy: Optional[StrategyEnum] = None
    priority: Optional[PriorityEnum] = None

class PHMHiringRequestRead(PHMHiringRequestBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# PHASE 2
class PHMPositionPrepBase(BaseModel):
    hiring_request_id: int
    position_type: PositionTypeEnum
    is_critical_position: bool = False
    critical_department: Optional[str] = None
    kras: Optional[Dict[str, Any]] = None
    kpis: Optional[Dict[str, Any]] = None
    soft_skills_required: Optional[Dict[str, Any]] = None
    task_list: Optional[Dict[str, Any]] = None
    process_steps: Optional[Dict[str, Any]] = None

class PHMPositionPrepCreate(PHMPositionPrepBase):
    pass

class PHMPositionPrepUpdate(PHMPositionPrepBase):
    hiring_request_id: Optional[int] = None
    position_type: Optional[PositionTypeEnum] = None

class PHMPositionPrepRead(PHMPositionPrepBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# PHASE 3
class PHMIdealCandidateProfileBase(BaseModel):
    position_prep_id: int
    functional_skills: Optional[List[str]] = None
    soft_skills_weightage: Optional[Dict[str, Any]] = None

class PHMIdealCandidateProfileCreate(PHMIdealCandidateProfileBase):
    pass

class PHMIdealCandidateProfileUpdate(PHMIdealCandidateProfileBase):
    position_prep_id: Optional[int] = None

class PHMIdealCandidateProfileRead(PHMIdealCandidateProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMInterviewQuestionBankBase(BaseModel):
    icp_id: int
    skill_type: SkillTypeEnum
    question: str
    expected_answer: Optional[str] = None
    max_score: int = 10

class PHMInterviewQuestionBankCreate(PHMInterviewQuestionBankBase):
    pass

class PHMInterviewQuestionBankUpdate(PHMInterviewQuestionBankBase):
    icp_id: Optional[int] = None
    skill_type: Optional[SkillTypeEnum] = None
    question: Optional[str] = None

class PHMInterviewQuestionBankRead(PHMInterviewQuestionBankBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# PHASE 4
class PHMSourcingChannelBase(BaseModel):
    name: str
    channel_type: ChannelTypeEnum

class PHMSourcingChannelCreate(PHMSourcingChannelBase):
    pass

class PHMSourcingChannelUpdate(PHMSourcingChannelBase):
    name: Optional[str] = None
    channel_type: Optional[ChannelTypeEnum] = None

class PHMSourcingChannelRead(PHMSourcingChannelBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMJobDescriptionBase(BaseModel):
    position_prep_id: int
    title: str
    summary: Optional[str] = None
    responsibilities: Optional[str] = None
    qualifications: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    perks: Optional[str] = None
    ad_copy: Optional[str] = None

class PHMJobDescriptionCreate(PHMJobDescriptionBase):
    pass

class PHMJobDescriptionUpdate(PHMJobDescriptionBase):
    position_prep_id: Optional[int] = None
    title: Optional[str] = None

class PHMJobDescriptionRead(PHMJobDescriptionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# PHASE 5
class PHMPipelineStageBase(BaseModel):
    name: str
    sequence: int = 0
    position_prep_id: Optional[int] = None

class PHMPipelineStageCreate(PHMPipelineStageBase):
    pass

class PHMPipelineStageUpdate(PHMPipelineStageBase):
    name: Optional[str] = None

class PHMPipelineStageRead(PHMPipelineStageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMRejectionReasonBase(BaseModel):
    reason_name: str

class PHMRejectionReasonCreate(PHMRejectionReasonBase):
    pass

class PHMRejectionReasonUpdate(PHMRejectionReasonBase):
    reason_name: Optional[str] = None

class PHMRejectionReasonRead(PHMRejectionReasonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMCandidateBase(BaseModel):
    name: str
    email: str
    resume_url: Optional[str] = None
    hiring_request_id: int
    stage_id: Optional[int] = None
    source_channel_id: Optional[int] = None
    rejection_reason_id: Optional[int] = None
    status: str = "active"

class PHMCandidateCreate(PHMCandidateBase):
    pass

class PHMCandidateUpdate(PHMCandidateBase):
    name: Optional[str] = None
    email: Optional[str] = None
    hiring_request_id: Optional[int] = None

class PHMCandidateRead(PHMCandidateBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# PHASE 6
class PHMCandidateScreeningBase(BaseModel):
    candidate_id: int
    cv_education_consistency: bool = False
    cv_type: Optional[CVTypeEnum] = None
    icp_match_score: Optional[float] = None

class PHMCandidateScreeningCreate(PHMCandidateScreeningBase):
    pass

class PHMCandidateScreeningUpdate(PHMCandidateScreeningBase):
    candidate_id: Optional[int] = None

class PHMCandidateScreeningRead(PHMCandidateScreeningBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMInterviewFeedbackBase(BaseModel):
    candidate_id: int
    round_name: RoundNameEnum
    panel_member: Optional[str] = None
    rating: Optional[float] = None
    feedback_text: Optional[str] = None
    is_cleared: bool = False

class PHMInterviewFeedbackCreate(PHMInterviewFeedbackBase):
    pass

class PHMInterviewFeedbackUpdate(PHMInterviewFeedbackBase):
    candidate_id: Optional[int] = None

class PHMInterviewFeedbackRead(PHMInterviewFeedbackBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMHiringErrorFlagBase(BaseModel):
    candidate_id: int
    error_type: ErrorTypeEnum
    notes: Optional[str] = None

class PHMHiringErrorFlagCreate(PHMHiringErrorFlagBase):
    pass

class PHMHiringErrorFlagUpdate(PHMHiringErrorFlagBase):
    candidate_id: Optional[int] = None
    error_type: Optional[ErrorTypeEnum] = None

class PHMHiringErrorFlagRead(PHMHiringErrorFlagBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# PROCESS ORCHESTRATION
class PHMHiringMasterTemplateBase(BaseModel):
    name: str
    version: str

class PHMHiringMasterTemplateCreate(PHMHiringMasterTemplateBase):
    pass

class PHMHiringMasterTemplateUpdate(PHMHiringMasterTemplateBase):
    name: Optional[str] = None
    version: Optional[str] = None

class PHMHiringMasterTemplateRead(PHMHiringMasterTemplateBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMMasterProcessStepBase(BaseModel):
    template_id: int
    step_number: int
    pipeline_stage_id: Optional[int] = None
    step_title: str
    step_description: Optional[str] = None
    estimated_hours: Optional[int] = None
    responsible_role: ResponsibleRoleEnum
    order_index: int

class PHMMasterProcessStepCreate(PHMMasterProcessStepBase):
    pass

class PHMMasterProcessStepUpdate(PHMMasterProcessStepBase):
    template_id: Optional[int] = None
    step_number: Optional[int] = None

class PHMMasterProcessStepRead(PHMMasterProcessStepBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMStepDependencyBase(BaseModel):
    step_id: int
    depends_on_step_id: int

class PHMStepDependencyCreate(PHMStepDependencyBase):
    pass

class PHMStepDependencyUpdate(PHMStepDependencyBase):
    step_id: Optional[int] = None
    depends_on_step_id: Optional[int] = None

class PHMStepDependencyRead(PHMStepDependencyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PHMRequestStepTrackerBase(BaseModel):
    hiring_request_id: int
    step_id: int
    assigned_to_user_id: Optional[int] = None
    status: TrackerStatusEnum = TrackerStatusEnum.NOT_STARTED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    blocker_notes: Optional[str] = None

class PHMRequestStepTrackerCreate(PHMRequestStepTrackerBase):
    pass

class PHMRequestStepTrackerUpdate(PHMRequestStepTrackerBase):
    hiring_request_id: Optional[int] = None
    step_id: Optional[int] = None

class PHMRequestStepTrackerRead(PHMRequestStepTrackerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# OFFER MANAGEMENT
class PHMOfferDetailsBase(BaseModel):
    candidate_id: int
    hiring_request_id: int
    offered_ctc: float
    offer_letter_sent_at: Optional[datetime] = None
    offer_accepted_at: Optional[datetime] = None
    joining_date: Optional[date] = None
    status: OfferStatusEnum = OfferStatusEnum.DRAFT

class PHMOfferDetailsCreate(PHMOfferDetailsBase):
    pass

class PHMOfferDetailsUpdate(PHMOfferDetailsBase):
    candidate_id: Optional[int] = None
    hiring_request_id: Optional[int] = None
    offered_ctc: Optional[float] = None

class PHMOfferDetailsRead(PHMOfferDetailsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# INTERVIEW SCHEDULING
class PHMInterviewScheduleBase(BaseModel):
    candidate_id: int
    round_name: RoundNameEnum
    interviewer_id: int
    scheduled_at: datetime
    duration_minutes: int = 60
    meeting_link: Optional[str] = None
    status: str = "scheduled"

class PHMInterviewScheduleCreate(PHMInterviewScheduleBase):
    pass

class PHMInterviewScheduleUpdate(PHMInterviewScheduleBase):
    candidate_id: Optional[int] = None
    round_name: Optional[RoundNameEnum] = None
    interviewer_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None

class PHMInterviewScheduleRead(PHMInterviewScheduleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
