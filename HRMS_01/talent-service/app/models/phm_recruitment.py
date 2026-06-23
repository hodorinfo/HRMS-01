from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from horilla_common.base import Base, HorillaBaseMixin
import enum

class TriggerEnum(str, enum.Enum):
    NOT_GETTING_RESULTS = "not_getting_results"
    BACKFILL = "backfill"
    OWNER_MOVING = "owner_moving"
    SPLIT_ROLE = "split_role"
    POOR_RESULTS = "poor_results"

class StrategyEnum(str, enum.Enum):
    DEVELOP_EXISTING = "develop_existing"
    HIRE_NEW = "hire_new"

class PriorityEnum(str, enum.Enum):
    IMMEDIATE = "immediate"
    CAN_WAIT = "can_wait"

class HiringRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class PositionTypeEnum(str, enum.Enum):
    MANAGER = "manager"
    DOER = "doer"

class SkillTypeEnum(str, enum.Enum):
    FUNCTIONAL = "functional"
    SOFT = "soft"

class ChannelTypeEnum(str, enum.Enum):
    PORTAL = "portal"
    REFERRAL = "referral"
    DIGITAL = "digital"

class CVTypeEnum(str, enum.Enum):
    TRANSACTIONAL = "transactional"
    MANAGERIAL = "managerial"

class ErrorTypeEnum(str, enum.Enum):
    MIXING_LEVELS = "mixing_levels"
    GROOM_VS_NEW = "groom_vs_new"
    BUDGET_ONLY = "budget_only"
    HIRE_FIRST_ALLOCATE_LATER = "hire_first_allocate_later"

# PHASE 1: WHEN TO HIRE
class PHMHiringRequest(Base, HorillaBaseMixin):
    __tablename__ = "phm_hiring_request"
    title: Mapped[str] = mapped_column(String(150))
    trigger: Mapped[TriggerEnum] = mapped_column(String(50))
    strategy: Mapped[StrategyEnum] = mapped_column(String(50))
    priority: Mapped[PriorityEnum] = mapped_column(String(50))
    roi_expensive_hire_cost: Mapped[float] = mapped_column(Float, default=0.0)
    roi_cheap_hire_cost: Mapped[float] = mapped_column(Float, default=0.0)
    roi_expected_return: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[HiringRequestStatus] = mapped_column(String(50), default=HiringRequestStatus.PENDING)

# PHASE 2: PREPARE FOR HIRING (P.T.S.T.D.M)
class PHMPositionPrep(Base, HorillaBaseMixin):
    __tablename__ = "phm_position_prep"
    hiring_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_request.id", ondelete="CASCADE"), unique=True)
    position_type: Mapped[PositionTypeEnum] = mapped_column(String(20))
    is_critical_position: Mapped[bool] = mapped_column(Boolean, default=False)
    critical_department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    kras: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    kpis: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    soft_skills_required: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    task_list: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    process_steps: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

# PHASE 3: IDEAL CANDIDATE PROFILE (ICP)
class PHMIdealCandidateProfile(Base, HorillaBaseMixin):
    __tablename__ = "phm_icp"
    position_prep_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_position_prep.id", ondelete="CASCADE"), unique=True)
    functional_skills: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    soft_skills_weightage: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class PHMInterviewQuestionBank(Base, HorillaBaseMixin):
    __tablename__ = "phm_interview_question_bank"
    icp_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_icp.id", ondelete="CASCADE"))
    skill_type: Mapped[SkillTypeEnum] = mapped_column(String(20))
    question: Mapped[str] = mapped_column(Text)
    expected_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    max_score: Mapped[int] = mapped_column(Integer, default=10)

# PHASE 4: SOURCE CANDIDATES
class PHMSourcingChannel(Base, HorillaBaseMixin):
    __tablename__ = "phm_sourcing_channel"
    name: Mapped[str] = mapped_column(String(100))
    channel_type: Mapped[ChannelTypeEnum] = mapped_column(String(20))

class PHMJobDescription(Base, HorillaBaseMixin):
    __tablename__ = "phm_job_description"
    position_prep_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_position_prep.id", ondelete="CASCADE"), unique=True)
    title: Mapped[str] = mapped_column(String(150))
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    responsibilities: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    qualifications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    salary_range_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_range_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    perks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ad_copy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# PHASE 5: HIRING PIPELINE (FUNNEL)
class PHMPipelineStage(Base, HorillaBaseMixin):
    __tablename__ = "phm_pipeline_stage"
    name: Mapped[str] = mapped_column(String(100))
    sequence: Mapped[int] = mapped_column(Integer, default=0)
    position_prep_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("phm_position_prep.id", ondelete="CASCADE"), nullable=True)

class PHMCandidate(Base, HorillaBaseMixin):
    __tablename__ = "phm_candidate"
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(254))
    hiring_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_request.id", ondelete="CASCADE"))
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_pipeline_stage.id", ondelete="SET NULL"), nullable=True)
    source_channel_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("phm_sourcing_channel.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")

# PHASE 6: SCREEN CANDIDATES
class PHMCandidateScreening(Base, HorillaBaseMixin):
    __tablename__ = "phm_candidate_screening"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"), unique=True)
    cv_education_consistency: Mapped[bool] = mapped_column(Boolean, default=False)
    cv_type: Mapped[Optional[CVTypeEnum]] = mapped_column(String(20), nullable=True)
    icp_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

class PHMTelephonicRound(Base, HorillaBaseMixin):
    __tablename__ = "phm_telephonic_round"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"), unique=True)
    start_hobbies_city: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    middle_skills_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    end_priorities: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sell_job_pitch: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class PHMHiringErrorFlag(Base, HorillaBaseMixin):
    __tablename__ = "phm_hiring_error_flag"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"))
    error_type: Mapped[ErrorTypeEnum] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
