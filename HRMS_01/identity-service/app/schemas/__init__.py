"""Identity Pydantic schemas."""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_staff: bool = False
    is_superuser: bool = False

class UserRead(HorillaSchema):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_staff: bool
    is_superuser: bool
    is_active: bool = True

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
    is_active: bool = True

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
