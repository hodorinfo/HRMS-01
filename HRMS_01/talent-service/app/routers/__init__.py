from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import (
    Objective, EmployeeObjective, Feedback, Offboarding, ResignationLetter, 
    OnboardingStage, OnboardingTask, CandidateStage, CandidateTask, OnboardingPortal,
    Period, KeyResult, OffboardingStage, OffboardingEmployee, OffboardingTask, EmployeeTask,
    ExitReason, OffboardingNote, OffboardingGeneralSetting, OffboardingStageMultipleFile
)
from app.schemas import (
    ObjectiveCreate, ObjectiveRead,
    EmployeeObjectiveCreate, EmployeeObjectiveRead,
    FeedbackCreate, FeedbackRead,
    OffboardingCreate, OffboardingRead,
    OffboardingStageFileCreate, OffboardingStageFileRead,
    ResignationLetterCreate, ResignationLetterRead,
    OnboardingStageCreate, OnboardingStageRead,
    OnboardingTaskCreate, OnboardingTaskRead,
    CandidateStageCreate, CandidateStageRead,
    CandidateTaskCreate, CandidateTaskRead,
    OnboardingPortalCreate, OnboardingPortalRead,
    PeriodCreate, PeriodRead,
    KeyResultCreate, KeyResultRead,
    OffboardingStageCreate, OffboardingStageRead,
    OffboardingEmployeeCreate, OffboardingEmployeeRead,
    OffboardingTaskCreate, OffboardingTaskRead,
    EmployeeTaskCreate, EmployeeTaskRead,
    ExitReasonCreate, ExitReasonRead,
    OffboardingNoteCreate, OffboardingNoteRead,
    OffboardingGeneralSettingCreate, OffboardingGeneralSettingRead,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read, module_name in [
    ("/objectives", Objective, ObjectiveCreate, ObjectiveRead, ObjectiveRead, "PMS (OKR)"), 
    ("/employee-objectives", EmployeeObjective, EmployeeObjectiveCreate, EmployeeObjectiveRead, EmployeeObjectiveRead, "PMS (OKR)"), 
    ("/periods", Period, PeriodCreate, PeriodRead, PeriodRead, "PMS (OKR)"),
    ("/key-results", KeyResult, KeyResultCreate, KeyResultRead, KeyResultRead, "PMS (OKR)"),
    ("/feedback", Feedback, FeedbackCreate, FeedbackRead, FeedbackRead, "PMS (Feedback)"), 
    ("/offboarding", Offboarding, OffboardingCreate, OffboardingRead, OffboardingRead, "Offboarding"), 
    ("/offboarding-stages", OffboardingStage, OffboardingStageCreate, OffboardingStageRead, OffboardingStageRead, "Offboarding"),
    ("/offboarding-employees", OffboardingEmployee, OffboardingEmployeeCreate, OffboardingEmployeeRead, OffboardingEmployeeRead, "Offboarding"),
    ("/offboarding-tasks", OffboardingTask, OffboardingTaskCreate, OffboardingTaskRead, OffboardingTaskRead, "Offboarding"),
    ("/employee-tasks", EmployeeTask, EmployeeTaskCreate, EmployeeTaskRead, EmployeeTaskRead, "Offboarding"),
    ("/resignation-letters", ResignationLetter, ResignationLetterCreate, ResignationLetterRead, ResignationLetterRead, "Offboarding"),
    ("/exit-reasons", ExitReason, ExitReasonCreate, ExitReasonRead, ExitReasonRead, "Offboarding"),
    ("/offboarding-notes", OffboardingNote, OffboardingNoteCreate, OffboardingNoteRead, OffboardingNoteRead, "Offboarding"),
    ("/offboarding-settings", OffboardingGeneralSetting, OffboardingGeneralSettingCreate, OffboardingGeneralSettingRead, OffboardingGeneralSettingRead, "Offboarding"),
    ("/offboarding-files", OffboardingStageMultipleFile, OffboardingStageFileCreate, OffboardingStageFileRead, OffboardingStageFileRead, "Offboarding"),
    ("/onboarding-stages", OnboardingStage, OnboardingStageCreate, OnboardingStageRead, OnboardingStageRead, "Onboarding"),
    ("/onboarding-tasks", OnboardingTask, OnboardingTaskCreate, OnboardingTaskRead, OnboardingTaskRead, "Onboarding"),
    ("/candidate-stages", CandidateStage, CandidateStageCreate, CandidateStageRead, CandidateStageRead, "Onboarding"),
    ("/candidate-tasks", CandidateTask, CandidateTaskCreate, CandidateTaskRead, CandidateTaskRead, "Onboarding"),
    ("/onboarding-portals", OnboardingPortal, OnboardingPortalCreate, OnboardingPortalRead, OnboardingPortalRead, "Onboarding"),
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, module_name))

# --- THESE ARE THE NEW RECRUITMENT ENDPOINTS (PHM 2.0) ---
from app.routers import phm_recruitment
api_router.include_router(phm_recruitment.router)
