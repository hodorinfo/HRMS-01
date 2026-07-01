"""Identity Pydantic schemas."""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_staff: bool = False
    is_superuser: bool = False

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: Optional[int] = None
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_staff: bool
    is_superuser: bool
    is_active: bool = True
    last_login: Optional[datetime] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class SetEmployeePasswordRequest(BaseModel):
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class EmployeeCreate(BaseModel):
    employee_first_name: str
    employee_last_name: Optional[str] = None
    email: EmailStr
    phone: str
    badge_id: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = "male"
    qualification: Optional[str] = None
    experience: Optional[int] = None
    marital_status: Optional[str] = "single"
    children: Optional[int] = None
    emergency_contact: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    additional_info: Optional[dict] = None
    password: Optional[str] = None

class EmployeeUpdate(BaseModel):
    employee_first_name: Optional[str] = None
    employee_last_name: Optional[str] = None
    phone: Optional[str] = None
    badge_id: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[int] = None
    marital_status: Optional[str] = None
    children: Optional[int] = None
    emergency_contact: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    is_active: Optional[bool] = None
    additional_info: Optional[dict] = None

class EmployeeTagRead(HorillaSchema):
    id: int
    title: Optional[str] = None
    color: Optional[str] = None
    is_active: bool = True

class EmployeeRead(HorillaSchema):
    id: int
    badge_id: Optional[str] = None
    employee_user_id: Optional[int] = None
    employee_first_name: str
    employee_last_name: Optional[str] = None
    employee_profile: Optional[str] = None
    email: str
    phone: str
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[int] = None
    marital_status: Optional[str] = None
    children: Optional[int] = None
    emergency_contact: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    is_active: bool = True
    additional_info: Optional[dict] = None
    is_from_onboarding: Optional[bool] = None
    is_directly_converted: Optional[bool] = None

class EmployeeWorkInformationCreate(BaseModel):
    employee_id: int
    department_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_role_id: Optional[int] = None
    reporting_manager_id: Optional[int] = None
    shift_id: Optional[int] = None
    work_type_id: Optional[int] = None
    employee_type_id: Optional[int] = None
    location: Optional[str] = None
    company_id: Optional[int] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    date_joining: Optional[date] = None
    contract_end_date: Optional[date] = None
    basic_salary: Optional[int] = 0
    salary_hour: Optional[int] = 0
    additional_info: Optional[dict] = None
    experience: Optional[float] = 0
    tag_ids: Optional[list[int]] = None

class EmployeeWorkInformationUpdate(EmployeeWorkInformationCreate):
    employee_id: Optional[int] = None

class EmployeeWorkInformationRead(HorillaSchema):
    id: int
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_role_id: Optional[int] = None
    reporting_manager_id: Optional[int] = None
    shift_id: Optional[int] = None
    work_type_id: Optional[int] = None
    employee_type_id: Optional[int] = None
    location: Optional[str] = None
    company_id: Optional[int] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    date_joining: Optional[date] = None
    contract_end_date: Optional[date] = None
    basic_salary: Optional[int] = None
    salary_hour: Optional[int] = None
    additional_info: Optional[dict] = None
    experience: Optional[float] = None

class EmployeeBankDetailsCreate(BaseModel):
    employee_id: int
    bank_name: str
    account_number: Optional[str] = None
    branch: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    any_other_code1: Optional[str] = None
    any_other_code2: Optional[str] = None
    additional_info: Optional[dict] = None

class EmployeeBankDetailsUpdate(BaseModel):
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    branch: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    any_other_code1: Optional[str] = None
    any_other_code2: Optional[str] = None
    additional_info: Optional[dict] = None

class EmployeeBankDetailsRead(HorillaSchema):
    id: int
    employee_id: Optional[int] = None
    bank_name: str
    account_number: Optional[str] = None
    branch: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    any_other_code1: Optional[str] = None
    any_other_code2: Optional[str] = None
    additional_info: Optional[dict] = None

class EmployeeListItemRead(EmployeeRead):
    work_info: Optional[EmployeeWorkInformationRead] = None

class EmployeeProfileRead(EmployeeRead):
    work_info: Optional[EmployeeWorkInformationRead] = None
    bank_details: Optional[EmployeeBankDetailsRead] = None

class LDAPSettingsCreate(BaseModel):
    ldap_server: str = "ldap://127.0.0.1:389"
    bind_dn: Optional[str] = None
    bind_password: Optional[str] = None
    base_dn: Optional[str] = None

class LDAPSettingsUpdate(LDAPSettingsCreate):
    pass

class LDAPSettingsRead(HorillaSchema):
    id: int
    ldap_server: str
    bind_dn: Optional[str] = None
    base_dn: Optional[str] = None

class DefaultAccessibilityCreate(BaseModel):
    feature: str
    filter: Optional[dict] = None
    exclude_all: bool = False
    is_enabled: bool = True

class DefaultAccessibilityUpdate(BaseModel):
    feature: Optional[str] = None
    filter: Optional[dict] = None
    exclude_all: Optional[bool] = None
    is_enabled: Optional[bool] = None

class DefaultAccessibilityRead(HorillaSchema):
    id: int
    feature: str
    filter: Optional[dict] = None
    exclude_all: bool = False
    is_enabled: bool = True
    is_active: bool = True

class AzureApiCreate(BaseModel):
    outlook_client_id: Optional[str] = None
    outlook_client_secret: Optional[str] = None
    outlook_tenant_id: Optional[str] = None
    outlook_email: Optional[str] = None
    outlook_display_name: Optional[str] = None
    outlook_redirect_uri: Optional[str] = None
    company_id: Optional[int] = None
    is_primary: bool = False

class AzureApiUpdate(AzureApiCreate):
    pass

class AzureApiRead(HorillaSchema):
    id: int
    outlook_client_id: Optional[str] = None
    outlook_tenant_id: Optional[str] = None
    outlook_email: Optional[str] = None
    outlook_display_name: Optional[str] = None
    company_id: Optional[int] = None
    is_primary: bool = False

class EmployeeNoteCreate(BaseModel):
    employee_id: int
    description: Optional[str] = None
    updated_by_id: Optional[int] = None

class EmployeeNoteUpdate(BaseModel):
    description: Optional[str] = None
    updated_by_id: Optional[int] = None

class EmployeeNoteRead(HorillaSchema):
    id: int
    employee_id: int
    description: Optional[str] = None
    updated_by_id: Optional[int] = None
    is_active: bool = True

class EmployeeTagCreate(BaseModel):
    title: Optional[str] = None
    color: Optional[str] = None

class EmployeeTagUpdate(EmployeeTagCreate):
    pass


class ActiontypeCreate(BaseModel):
    title: str
    action_type: str
    block_option: bool = False

class ActiontypeUpdate(BaseModel):
    title: Optional[str] = None
    action_type: Optional[str] = None
    block_option: Optional[bool] = None

class ActiontypeRead(HorillaSchema):
    id: int
    title: str
    action_type: str
    block_option: bool
    is_active: bool = True

class DisciplinaryActionCreate(BaseModel):
    employee_ids: list[int]
    action_id: int
    description: Optional[str] = None
    unit_in: str = "days"
    days: Optional[int] = 1
    hours: str = "00:00"
    start_date: Optional[date] = None
    attachment: Optional[str] = None

class DisciplinaryActionUpdate(BaseModel):
    employee_ids: Optional[list[int]] = None
    action_id: Optional[int] = None
    description: Optional[str] = None
    unit_in: Optional[str] = None
    days: Optional[int] = None
    hours: Optional[str] = None
    start_date: Optional[date] = None
    attachment: Optional[str] = None

class DisciplinaryActionRead(HorillaSchema):
    id: int
    employee_ids: list[int] = []
    action_id: int
    description: Optional[str] = None
    unit_in: str
    days: Optional[int] = None
    hours: str
    start_date: Optional[date] = None
    attachment: Optional[str] = None
    is_active: bool = True

class DisciplinaryBulkIdsRequest(BaseModel):
    ids: list[int]

class DisciplinaryBulkActionResponse(BaseModel):
    updated_count: int
    failed_count: int = 0
    errors: Optional[list[str]] = None

class BonusPointCreate(BaseModel):
    employee_id: Optional[int] = None
    points: int = 0
    encashment_condition: Optional[str] = None
    redeeming_points: Optional[int] = None
    reason: Optional[str] = None

class BonusPointUpdate(BaseModel):
    employee_id: Optional[int] = None
    points: Optional[int] = None
    encashment_condition: Optional[str] = None
    redeeming_points: Optional[int] = None
    reason: Optional[str] = None

class BonusPointRead(HorillaSchema):
    id: int
    employee_id: Optional[int] = None
    points: int
    encashment_condition: Optional[str] = None
    redeeming_points: Optional[int] = None
    reason: Optional[str] = None
    is_active: bool = True

class PolicyCreate(BaseModel):
    title: str
    body: str
    is_visible_to_all: bool = True

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    is_visible_to_all: Optional[bool] = None

class PolicyRead(HorillaSchema):
    id: int
    title: str
    body: str
    is_visible_to_all: bool
    is_active: bool = True

class EmployeeGeneralSettingCreate(BaseModel):
    badge_id_prefix: str = "EMP"
    company_id: Optional[int] = None

class EmployeeGeneralSettingUpdate(BaseModel):
    badge_id_prefix: Optional[str] = None
    company_id: Optional[int] = None

class EmployeeGeneralSettingRead(HorillaSchema):
    id: int
    badge_id_prefix: str
    company_id: Optional[int] = None
    is_active: bool = True

class ProfileEditFeatureCreate(BaseModel):
    is_enabled: bool = False

class ProfileEditFeatureUpdate(BaseModel):
    is_enabled: Optional[bool] = None

class ProfileEditFeatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_enabled: bool
    is_active: bool = True
