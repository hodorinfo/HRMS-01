from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Recruitment, Candidate, Objective, EmployeeObjective, Feedback, Offboarding, ResignationLetter
from app.schemas import (
    RecruitmentCreate, RecruitmentUpdate, RecruitmentRead,
    CandidateCreate, CandidateUpdate, CandidateRead,
    ObjectiveCreate, ObjectiveCreate, ObjectiveRead,
    EmployeeObjectiveCreate, EmployeeObjectiveCreate, EmployeeObjectiveRead,
    FeedbackCreate, FeedbackCreate, FeedbackRead,
    OffboardingCreate, OffboardingCreate, OffboardingRead,
    ResignationLetterCreate, ResignationLetterCreate, ResignationLetterRead,
)
from app.routers import health

api_router = APIRouter()
api_router.include_router(health.router)
for prefix, model, create, update, read in [
    ("/recruitment", Recruitment, RecruitmentCreate, RecruitmentUpdate, RecruitmentRead),
    ("/candidates", Candidate, CandidateCreate, CandidateUpdate, CandidateRead),
    ("/objectives", Objective, ObjectiveCreate, ObjectiveRead, ObjectiveRead), # TODO: Fix update schema
    ("/employee-objectives", EmployeeObjective, EmployeeObjectiveCreate, EmployeeObjectiveRead, EmployeeObjectiveRead), # TODO: Fix update schema
    ("/feedback", Feedback, FeedbackCreate, FeedbackRead, FeedbackRead), # TODO: Fix update schema
    ("/offboarding", Offboarding, OffboardingCreate, OffboardingRead, OffboardingRead), # TODO: Fix update schema
    ("/resignation-letters", ResignationLetter, ResignationLetterCreate, ResignationLetterRead, ResignationLetterRead), # TODO: Fix update schema
]:
    api_router.include_router(create_crud_router(prefix, model, create, update, read, get_db, get_current_user, "recruitment"))
