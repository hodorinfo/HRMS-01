from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user

# Models
from app.models import (
    PHMHiringRequest, PHMPositionPrep, PHMIdealCandidateProfile, PHMInterviewQuestionBank,
    PHMSourcingChannel, PHMJobDescription, PHMPipelineStage, PHMRejectionReason, PHMCandidate,
    PHMCandidateScreening, PHMInterviewFeedback, PHMHiringErrorFlag,
    PHMHiringMasterTemplate, PHMMasterProcessStep, PHMStepDependency, PHMRequestStepTracker, PHMOfferDetails
)

# Schemas
from app.schemas import (
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

router = APIRouter()

# Register all routes dynamically using the CRUD router
routers = [
    ("/hiring-requests", PHMHiringRequest, PHMHiringRequestCreate, PHMHiringRequestUpdate, PHMHiringRequestRead, "PHM: Requests & Prep"),
    ("/position-preps", PHMPositionPrep, PHMPositionPrepCreate, PHMPositionPrepUpdate, PHMPositionPrepRead, "PHM: Requests & Prep"),
    ("/icps", PHMIdealCandidateProfile, PHMIdealCandidateProfileCreate, PHMIdealCandidateProfileUpdate, PHMIdealCandidateProfileRead, "PHM: Requests & Prep"),
    ("/interview-questions", PHMInterviewQuestionBank, PHMInterviewQuestionBankCreate, PHMInterviewQuestionBankUpdate, PHMInterviewQuestionBankRead, "PHM: Requests & Prep"),
    ("/job-descriptions", PHMJobDescription, PHMJobDescriptionCreate, PHMJobDescriptionUpdate, PHMJobDescriptionRead, "PHM: Requests & Prep"),
    
    ("/sourcing-channels", PHMSourcingChannel, PHMSourcingChannelCreate, PHMSourcingChannelUpdate, PHMSourcingChannelRead, "PHM: Candidates & Pipeline"),
    ("/pipeline-stages", PHMPipelineStage, PHMPipelineStageCreate, PHMPipelineStageUpdate, PHMPipelineStageRead, "PHM: Candidates & Pipeline"),
    ("/rejection-reasons", PHMRejectionReason, PHMRejectionReasonCreate, PHMRejectionReasonUpdate, PHMRejectionReasonRead, "PHM: Candidates & Pipeline"),
    ("/candidates", PHMCandidate, PHMCandidateCreate, PHMCandidateUpdate, PHMCandidateRead, "PHM: Candidates & Pipeline"),
    ("/candidate-screenings", PHMCandidateScreening, PHMCandidateScreeningCreate, PHMCandidateScreeningUpdate, PHMCandidateScreeningRead, "PHM: Candidates & Pipeline"),
    ("/interview-feedbacks", PHMInterviewFeedback, PHMInterviewFeedbackCreate, PHMInterviewFeedbackUpdate, PHMInterviewFeedbackRead, "PHM: Candidates & Pipeline"),
    ("/hiring-error-flags", PHMHiringErrorFlag, PHMHiringErrorFlagCreate, PHMHiringErrorFlagUpdate, PHMHiringErrorFlagRead, "PHM: Candidates & Pipeline"),
    ("/offer-details", PHMOfferDetails, PHMOfferDetailsCreate, PHMOfferDetailsUpdate, PHMOfferDetailsRead, "PHM: Candidates & Pipeline"),
    
    ("/hiring-master-templates", PHMHiringMasterTemplate, PHMHiringMasterTemplateCreate, PHMHiringMasterTemplateUpdate, PHMHiringMasterTemplateRead, "PHM: Process Orchestration"),
    ("/master-process-steps", PHMMasterProcessStep, PHMMasterProcessStepCreate, PHMMasterProcessStepUpdate, PHMMasterProcessStepRead, "PHM: Process Orchestration"),
    ("/step-dependencies", PHMStepDependency, PHMStepDependencyCreate, PHMStepDependencyUpdate, PHMStepDependencyRead, "PHM: Process Orchestration"),
    ("/request-step-trackers", PHMRequestStepTracker, PHMRequestStepTrackerCreate, PHMRequestStepTrackerUpdate, PHMRequestStepTrackerRead, "PHM: Process Orchestration"),
]

for prefix, model, create_schema, update_schema, read_schema, module_tag in routers:
    crud_router = create_crud_router(
        prefix=prefix,
        model=model,
        create_schema=create_schema,
        update_schema=update_schema,
        read_schema=read_schema,
        get_db=get_db,
        get_current_user=get_current_user,
        module=module_tag
    )
    router.include_router(crud_router)
