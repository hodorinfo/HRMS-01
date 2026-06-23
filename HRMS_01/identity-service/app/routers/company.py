"""Company policies and general settings endpoints."""
from fastapi import APIRouter
from horilla_common.crud import create_crud_router
from app.database import get_db
from app.dependencies import get_current_user
from app.models import EmployeeGeneralSetting, Policy, ProfileEditFeature
from app.schemas import (
    EmployeeGeneralSettingCreate, EmployeeGeneralSettingRead, EmployeeGeneralSettingUpdate,
    PolicyCreate, PolicyRead, PolicyUpdate,
    ProfileEditFeatureCreate, ProfileEditFeatureRead, ProfileEditFeatureUpdate
)

router = APIRouter()
router.include_router(create_crud_router("/policies", Policy, PolicyCreate, PolicyUpdate, PolicyRead, get_db, get_current_user, "employee"))
router.include_router(create_crud_router("/general-settings", EmployeeGeneralSetting, EmployeeGeneralSettingCreate, EmployeeGeneralSettingUpdate, EmployeeGeneralSettingRead, get_db, get_current_user, "employee"))
router.include_router(create_crud_router("/profile-edit-features", ProfileEditFeature, ProfileEditFeatureCreate, ProfileEditFeatureUpdate, ProfileEditFeatureRead, get_db, get_current_user, "employee"))
