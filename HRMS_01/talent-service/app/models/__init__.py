from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from horilla_common.base import Base, HorillaBaseMixin

# Legacy recruitment models removed.


# PMS
class Period(Base, HorillaBaseMixin):
    __tablename__ = "pms_period"
    period_name: Mapped[str] = mapped_column(String(100), unique=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

class KeyResult(Base, HorillaBaseMixin):
    __tablename__ = "pms_keyresult"
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    progress_type: Mapped[str] = mapped_column(String(20), default="%")
    target_value: Mapped[int] = mapped_column(Integer, default=0)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    archive: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class Objective(Base, HorillaBaseMixin):
    __tablename__ = "pms_objective"
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_unit: Mapped[str] = mapped_column(String(10), default="days")
    duration: Mapped[int] = mapped_column(Integer, default=0)
    add_assignees: Mapped[bool] = mapped_column(Boolean, default=False)
    archive: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    self_employee_progress_update: Mapped[bool] = mapped_column(Boolean, default=False)

class EmployeeObjective(Base, HorillaBaseMixin):
    __tablename__ = "pms_employeeobjective"
    __table_args__ = (UniqueConstraint("employee_id", "objective_id", name="uq_emp_objective"),)
    objective: Mapped[str] = mapped_column(String(100))
    objective_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    objective_id: Mapped[int] = mapped_column(Integer, ForeignKey("pms_objective.id"))
    employee_id: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="Not Started")
    progress_percentage: Mapped[int] = mapped_column(Integer, default=0)
    archive: Mapped[bool] = mapped_column(Boolean, default=False)

class Feedback(Base, HorillaBaseMixin):
    __tablename__ = "pms_feedback"
    review_cycle: Mapped[str] = mapped_column(String(100))
    manager_id: Mapped[int] = mapped_column(Integer)
    employee_id: Mapped[int] = mapped_column(Integer)
    question_template_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    archive: Mapped[bool] = mapped_column(Boolean, default=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cyclic_feedback: Mapped[bool] = mapped_column(Boolean, default=False)

# Onboarding
class OnboardingStage(Base, HorillaBaseMixin):
    __tablename__ = "onboarding_onboardingstage"
    stage_title: Mapped[str] = mapped_column(String(100))
    recruitment_id: Mapped[int] = mapped_column(Integer, ForeignKey("phm_hiring_request.id"))
    employee_id: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, default=0)
    is_final_stage: Mapped[bool] = mapped_column(Boolean, default=False)

class OnboardingTask(Base, HorillaBaseMixin):
    __tablename__ = "onboarding_onboardingtask"
    task_title: Mapped[str] = mapped_column(String(100))
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_onboardingstage.id"))
    candidates: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    employee_id: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

class CandidateStage(Base, HorillaBaseMixin):
    __tablename__ = "onboarding_candidatestage"
    candidate_id: Mapped[int] = mapped_column(Integer, unique=True)
    onboarding_stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_onboardingstage.id"))
    onboarding_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, default=0)

class CandidateTask(Base, HorillaBaseMixin):
    __tablename__ = "onboarding_candidatetask"
    candidate_id: Mapped[int] = mapped_column(Integer)
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_onboardingstage.id"))
    onboarding_task_id: Mapped[int] = mapped_column(Integer, ForeignKey("onboarding_onboardingtask.id"))
    status: Mapped[str] = mapped_column(String(20), default="todo")
    history: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class OnboardingPortal(Base, HorillaBaseMixin):
    __tablename__ = "onboarding_onboardingportal"
    candidate_id: Mapped[int] = mapped_column(Integer, unique=True)
    token: Mapped[str] = mapped_column(String(100))
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    count: Mapped[int] = mapped_column(Integer, default=0)
    profile: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# Offboarding
class OffboardingStageMultipleFile(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_offboardingstagefile"
    attachment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class Offboarding(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_offboarding"
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    managers: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # M2M -> employee_ids
    status: Mapped[str] = mapped_column(String(20), default="ongoing")
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class OffboardingStage(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_offboardingstage"
    title: Mapped[str] = mapped_column(String(20))
    type: Mapped[str] = mapped_column(String(20), default="other")
    offboarding_id: Mapped[int] = mapped_column(Integer, ForeignKey("offboarding_offboarding.id"))
    managers: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # M2M -> employee_ids
    sequence: Mapped[int] = mapped_column(Integer, default=0)

class OffboardingEmployee(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_offboardingemployee"
    employee_id: Mapped[int] = mapped_column(Integer, unique=True)
    stage_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("offboarding_offboardingstage.id"), nullable=True)
    notice_period: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(10), default="month", nullable=True)
    notice_period_starts: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notice_period_ends: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

class ResignationLetter(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_resignationletter"
    employee_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    planned_to_leave_on: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="requested")
    offboarding_employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class OffboardingTask(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_offboardingtask"
    __table_args__ = (UniqueConstraint("title", "stage_id", name="uq_offboarding_task_title_stage"),)
    title: Mapped[str] = mapped_column(String(30))
    managers: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # M2M -> employee_ids
    stage_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("offboarding_offboardingstage.id"), nullable=True)

class EmployeeTask(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_employeetask"
    __table_args__ = (UniqueConstraint("employee_id", "task_id", name="uq_employee_task"),)
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("offboarding_offboardingemployee.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="todo")
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("offboarding_offboardingtask.id"))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    history: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

class ExitReason(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_exitreason"
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    offboarding_employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("offboarding_offboardingemployee.id"))
    attachments: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # M2M -> file_ids

class OffboardingNote(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_offboardingnote"
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    note_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # FK -> employee_id
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("offboarding_offboardingemployee.id"), nullable=True)
    stage_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("offboarding_offboardingstage.id"), nullable=True)
    attachments: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # M2M -> file_ids

class OffboardingGeneralSetting(Base, HorillaBaseMixin):
    __tablename__ = "offboarding_generalsetting"
    resignation_request: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

from .phm_recruitment import (
    PHMHiringRequest, PHMPositionPrep, PHMIdealCandidateProfile, PHMInterviewQuestionBank,
    PHMSourcingChannel, PHMJobDescription, PHMPipelineStage, PHMRejectionReason, PHMCandidate,
    PHMCandidateScreening, PHMInterviewFeedback, PHMHiringErrorFlag,
    PHMHiringMasterTemplate, PHMMasterProcessStep, PHMStepDependency, PHMRequestStepTracker, PHMOfferDetails,
    PHMInterviewSchedule
)
