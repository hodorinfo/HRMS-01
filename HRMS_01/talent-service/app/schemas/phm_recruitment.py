from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.phm_recruitment import (
    TriggerEnum, StrategyEnum, PriorityEnum, HiringRequestStatus, PositionTypeEnum,
    SkillTypeEnum, ChannelTypeEnum, CVTypeEnum, ErrorTypeEnum
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

class PHMCandidateBase(BaseModel):
    name: str
    email: str
    hiring_request_id: int
    stage_id: Optional[int] = None
    source_channel_id: Optional[int] = None
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

class PHMTelephonicRoundBase(BaseModel):
    candidate_id: int
    start_hobbies_city: Optional[str] = None
    middle_skills_rating: Optional[float] = None
    end_priorities: Optional[str] = None
    sell_job_pitch: Optional[str] = None

class PHMTelephonicRoundCreate(PHMTelephonicRoundBase):
    pass

class PHMTelephonicRoundUpdate(PHMTelephonicRoundBase):
    candidate_id: Optional[int] = None

class PHMTelephonicRoundRead(PHMTelephonicRoundBase):
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
