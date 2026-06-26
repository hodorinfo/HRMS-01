from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text, Date, DateTime, UniqueConstraint
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

class RoundNameEnum(str, enum.Enum):
    TELEPHONIC = "telephonic"
    ASSIGNMENT = "assignment"
    TECHNICAL = "technical"
    MANAGERIAL = "managerial"
    HR = "hr"

class ErrorTypeEnum(str, enum.Enum):
    MIXING_LEVELS = "mixing_levels"
    GROOM_VS_NEW = "groom_vs_new"
    BUDGET_ONLY = "budget_only"
    HIRE_FIRST_ALLOCATE_LATER = "hire_first_allocate_later"

class ResponsibleRoleEnum(str, enum.Enum):
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
    HRBP = "hrbp"
    COORDINATOR = "coordinator"

class TrackerStatusEnum(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class OfferStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    JOINED = "joined"

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
    target_hire_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    actual_filled_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
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

class PHMRejectionReason(Base): # No HorillaBaseMixin since it's just a lookup table with id & reason_name as requested, or maybe we just add it
    __tablename__ = "phm_rejection_reason"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reason_name: Mapped[str] = mapped_column(String(100), unique=True)

class PHMCandidate(Base, HorillaBaseMixin):
    __tablename__ = "phm_candidate"
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(254))
    resume_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hiring_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_request.id", ondelete="CASCADE"))
    stage_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("phm_pipeline_stage.id", ondelete="SET NULL"), nullable=True)
    source_channel_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("phm_sourcing_channel.id", ondelete="SET NULL"), nullable=True)
    rejection_reason_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("phm_rejection_reason.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")

# PHASE 6: SCREEN CANDIDATES
class PHMCandidateScreening(Base, HorillaBaseMixin):
    __tablename__ = "phm_candidate_screening"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"), unique=True)
    cv_education_consistency: Mapped[bool] = mapped_column(Boolean, default=False)
    cv_type: Mapped[Optional[CVTypeEnum]] = mapped_column(String(20), nullable=True)
    icp_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

class PHMInterviewFeedback(Base, HorillaBaseMixin):
    __tablename__ = "phm_interview_feedback"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"))
    round_name: Mapped[RoundNameEnum] = mapped_column(String(50))
    panel_member: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    feedback_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_cleared: Mapped[bool] = mapped_column(Boolean, default=False)

class PHMHiringErrorFlag(Base, HorillaBaseMixin):
    __tablename__ = "phm_hiring_error_flag"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"))
    error_type: Mapped[ErrorTypeEnum] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# PROCESS ORCHESTRATION TABLES
class PHMHiringMasterTemplate(Base, HorillaBaseMixin):
    __tablename__ = "phm_hiring_master_template"
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(20))

class PHMMasterProcessStep(Base, HorillaBaseMixin):
    __tablename__ = "phm_master_process_step"
    __table_args__ = (UniqueConstraint("template_id", "step_number"),)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_master_template.id", ondelete="CASCADE"))
    step_number: Mapped[int] = mapped_column(Integer)
    pipeline_stage_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("phm_pipeline_stage.id", ondelete="SET NULL"), nullable=True)
    step_title: Mapped[str] = mapped_column(String(255))
    step_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    responsible_role: Mapped[ResponsibleRoleEnum] = mapped_column(String(50))
    order_index: Mapped[int] = mapped_column(Integer)

class PHMStepDependency(Base):
    __tablename__ = "phm_step_dependency"
    __table_args__ = (UniqueConstraint("step_id", "depends_on_step_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    step_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_master_process_step.id", ondelete="CASCADE"))
    depends_on_step_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_master_process_step.id", ondelete="CASCADE"))

class PHMRequestStepTracker(Base, HorillaBaseMixin):
    __tablename__ = "phm_request_step_tracker"
    __table_args__ = (UniqueConstraint("hiring_request_id", "step_id"),)
    hiring_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_request.id", ondelete="CASCADE"))
    step_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_master_process_step.id", ondelete="CASCADE"))
    assigned_to_user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[TrackerStatusEnum] = mapped_column(String(50), default=TrackerStatusEnum.NOT_STARTED)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    blocker_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# OFFER MANAGEMENT
class PHMOfferDetails(Base, HorillaBaseMixin):
    __tablename__ = "phm_offer_details"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"), unique=True)
    hiring_request_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_request.id", ondelete="CASCADE"))
    offered_ctc: Mapped[float] = mapped_column(Float)
    offer_letter_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    offer_accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    joining_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[OfferStatusEnum] = mapped_column(String(50), default=OfferStatusEnum.DRAFT)

# INTERVIEW SCHEDULING
class PHMInterviewSchedule(Base, HorillaBaseMixin):
    __tablename__ = "phm_interview_schedule"
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_candidate.id", ondelete="CASCADE"))
    round_name: Mapped[RoundNameEnum] = mapped_column(String(50))
    interviewer_id: Mapped[int] = mapped_column(Integer)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    meeting_link: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")
