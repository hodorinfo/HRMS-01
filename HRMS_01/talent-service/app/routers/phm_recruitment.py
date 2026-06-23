from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user

# Models
from app.models import (
    PHMHiringRequest, PHMPositionPrep, PHMIdealCandidateProfile, PHMInterviewQuestionBank,
    PHMSourcingChannel, PHMJobDescription, PHMPipelineStage, PHMCandidate,
    PHMCandidateScreening, PHMTelephonicRound, PHMHiringErrorFlag
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
    PHMCandidateCreate, PHMCandidateUpdate, PHMCandidateRead,
    PHMCandidateScreeningCreate, PHMCandidateScreeningUpdate, PHMCandidateScreeningRead,
    PHMTelephonicRoundCreate, PHMTelephonicRoundUpdate, PHMTelephonicRoundRead,
    PHMHiringErrorFlagCreate, PHMHiringErrorFlagUpdate, PHMHiringErrorFlagRead
)

router = APIRouter()

# Register all routes dynamically using the CRUD router
routers = [
    ("/hiring-requests", PHMHiringRequest, PHMHiringRequestCreate, PHMHiringRequestUpdate, PHMHiringRequestRead),
    ("/position-preps", PHMPositionPrep, PHMPositionPrepCreate, PHMPositionPrepUpdate, PHMPositionPrepRead),
    ("/icps", PHMIdealCandidateProfile, PHMIdealCandidateProfileCreate, PHMIdealCandidateProfileUpdate, PHMIdealCandidateProfileRead),
    ("/interview-questions", PHMInterviewQuestionBank, PHMInterviewQuestionBankCreate, PHMInterviewQuestionBankUpdate, PHMInterviewQuestionBankRead),
    ("/sourcing-channels", PHMSourcingChannel, PHMSourcingChannelCreate, PHMSourcingChannelUpdate, PHMSourcingChannelRead),
    ("/job-descriptions", PHMJobDescription, PHMJobDescriptionCreate, PHMJobDescriptionUpdate, PHMJobDescriptionRead),
    ("/pipeline-stages", PHMPipelineStage, PHMPipelineStageCreate, PHMPipelineStageUpdate, PHMPipelineStageRead),
    ("/candidates", PHMCandidate, PHMCandidateCreate, PHMCandidateUpdate, PHMCandidateRead),
    ("/candidate-screenings", PHMCandidateScreening, PHMCandidateScreeningCreate, PHMCandidateScreeningUpdate, PHMCandidateScreeningRead),
    ("/telephonic-rounds", PHMTelephonicRound, PHMTelephonicRoundCreate, PHMTelephonicRoundUpdate, PHMTelephonicRoundRead),
    ("/hiring-error-flags", PHMHiringErrorFlag, PHMHiringErrorFlagCreate, PHMHiringErrorFlagUpdate, PHMHiringErrorFlagRead),
]

for prefix, model, create_schema, update_schema, read_schema in routers:
    crud_router = create_crud_router(
        prefix=prefix,
        model=model,
        create_schema=create_schema,
        update_schema=update_schema,
        read_schema=read_schema,
        get_db=get_db,
        get_current_user=get_current_user,
        module="PHM Recruitment"
    )
    router.include_router(crud_router)
