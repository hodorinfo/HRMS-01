# Identity Service API Documentation

Complete API reference for Identity Service.

**Service:** Identity Service  
**Port:** 8000 (Internal) / 8001 (Mapped)  
**Base URL (Direct):** `http://localhost:8001`  
**Base URL (Gateway):** `http://192.168.1.41` (via Nginx)  
**Container:** `hrms_01-identity-service-1`

**Authentication:** JWT Bearer Token (all API endpoints except health/login)  
**Schema:** `horilla_identity` (PostgreSQL)

---

## Endpoints

### Ping

**GET** `/api/v1/ping`

**Description:** No description provided.

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/ping \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```


### Login

**POST** `/api/v1/auth/login`

**Description:** No description provided.

**Request Body (Form):** Required fields according to OAuth2 password flow.

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/auth/login \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Refresh Token

**POST** `/api/v1/auth/refresh`

**Description:** No description provided.

**Query Parameters:**
- `refresh_token` (string)

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/auth/refresh \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Me

**GET** `/api/v1/auth/me`

**Description:** No description provided.

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/auth/me \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "is_staff": "boolean",
  "is_superuser": "boolean",
  "is_active": "boolean",
  "last_login": "string",
}
```


### Update Me

**PUT** `/api/v1/auth/me`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/auth/me \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "is_staff": "boolean",
  "is_superuser": "boolean",
  "is_active": "boolean",
  "last_login": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Register

**POST** `/api/v1/auth/register`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "is_staff": "boolean",
  "is_superuser": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/auth/register \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "is_staff": "boolean",
  "is_superuser": "boolean",
  "is_active": "boolean",
  "last_login": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Change Password

**POST** `/api/v1/auth/change-password`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "old_password": "string",
  "new_password": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/auth/change-password \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Forgot Password

**POST** `/api/v1/auth/forgot-password`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "email": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/auth/forgot-password \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Reset Password

**POST** `/api/v1/auth/reset-password`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "token": "string",
  "new_password": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/auth/reset-password \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### List Employees

**GET** `/api/v1/employees`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)
- `is_active` (string)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employees \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Employee

**POST** `/api/v1/employees`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_first_name": "string",
  "employee_last_name": "string",
  "email": "string",
  "phone": "string",
  "badge_id": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "zip": "string",
  "dob": "string",
  "gender": "string",
  "qualification": "string",
  "experience": "string",
  "marital_status": "string",
  "children": "string",
  "emergency_contact": "string",
  "emergency_contact_name": "string",
  "emergency_contact_relation": "string",
  "additional_info": "string",
  "password": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employees \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "badge_id": "string",
  "employee_user_id": "string",
  "employee_first_name": "string",
  "employee_last_name": "string",
  "employee_profile": "string",
  "email": "string",
  "phone": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "zip": "string",
  "dob": "string",
  "gender": "string",
  "qualification": "string",
  "experience": "string",
  "marital_status": "string",
  "children": "string",
  "emergency_contact": "string",
  "emergency_contact_name": "string",
  "emergency_contact_relation": "string",
  "is_active": "boolean",
  "additional_info": "string",
  "is_from_onboarding": "string",
  "is_directly_converted": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Employee

**GET** `/api/v1/employees/{employee_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employees/{employee_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "badge_id": "string",
  "employee_user_id": "string",
  "employee_first_name": "string",
  "employee_last_name": "string",
  "employee_profile": "string",
  "email": "string",
  "phone": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "zip": "string",
  "dob": "string",
  "gender": "string",
  "qualification": "string",
  "experience": "string",
  "marital_status": "string",
  "children": "string",
  "emergency_contact": "string",
  "emergency_contact_name": "string",
  "emergency_contact_relation": "string",
  "is_active": "boolean",
  "additional_info": "string",
  "is_from_onboarding": "string",
  "is_directly_converted": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Employee

**PUT** `/api/v1/employees/{employee_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "employee_first_name": "string",
  "employee_last_name": "string",
  "phone": "string",
  "badge_id": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "zip": "string",
  "dob": "string",
  "gender": "string",
  "qualification": "string",
  "experience": "string",
  "marital_status": "string",
  "children": "string",
  "emergency_contact": "string",
  "emergency_contact_name": "string",
  "emergency_contact_relation": "string",
  "is_active": "string",
  "additional_info": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/employees/{employee_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "badge_id": "string",
  "employee_user_id": "string",
  "employee_first_name": "string",
  "employee_last_name": "string",
  "employee_profile": "string",
  "email": "string",
  "phone": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "zip": "string",
  "dob": "string",
  "gender": "string",
  "qualification": "string",
  "experience": "string",
  "marital_status": "string",
  "children": "string",
  "emergency_contact": "string",
  "emergency_contact_name": "string",
  "emergency_contact_relation": "string",
  "is_active": "boolean",
  "additional_info": "string",
  "is_from_onboarding": "string",
  "is_directly_converted": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Employee

**DELETE** `/api/v1/employees/{employee_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/employees/{employee_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### Set Employee Password

**POST** `/api/v1/employees/{employee_id}/set-password`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "new_password": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employees/{employee_id}/set-password \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Send Invitation

**POST** `/api/v1/employees/{employee_id}/send-invitation`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employees/{employee_id}/send-invitation \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Toggle Employee Status

**POST** `/api/v1/employees/{employee_id}/toggle-status`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employees/{employee_id}/toggle-status \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/employees/work-info`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employees/work-info \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/employees/work-info`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "department_id": "string",
  "job_position_id": "string",
  "job_role_id": "string",
  "reporting_manager_id": "string",
  "shift_id": "string",
  "work_type_id": "string",
  "employee_type_id": "string",
  "location": "string",
  "company_id": "string",
  "email": "string",
  "mobile": "string",
  "date_joining": "string",
  "contract_end_date": "string",
  "basic_salary": "string",
  "salary_hour": "string",
  "additional_info": "string",
  "experience": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employees/work-info \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "department_id": "string",
  "job_position_id": "string",
  "job_role_id": "string",
  "reporting_manager_id": "string",
  "shift_id": "string",
  "work_type_id": "string",
  "employee_type_id": "string",
  "location": "string",
  "company_id": "string",
  "email": "string",
  "mobile": "string",
  "date_joining": "string",
  "contract_end_date": "string",
  "basic_salary": "string",
  "salary_hour": "string",
  "additional_info": "string",
  "experience": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/employees/work-info/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employees/work-info/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "department_id": "string",
  "job_position_id": "string",
  "job_role_id": "string",
  "reporting_manager_id": "string",
  "shift_id": "string",
  "work_type_id": "string",
  "employee_type_id": "string",
  "location": "string",
  "company_id": "string",
  "email": "string",
  "mobile": "string",
  "date_joining": "string",
  "contract_end_date": "string",
  "basic_salary": "string",
  "salary_hour": "string",
  "additional_info": "string",
  "experience": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/employees/work-info/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "employee_id": "string",
  "department_id": "string",
  "job_position_id": "string",
  "job_role_id": "string",
  "reporting_manager_id": "string",
  "shift_id": "string",
  "work_type_id": "string",
  "employee_type_id": "string",
  "location": "string",
  "company_id": "string",
  "email": "string",
  "mobile": "string",
  "date_joining": "string",
  "contract_end_date": "string",
  "basic_salary": "string",
  "salary_hour": "string",
  "additional_info": "string",
  "experience": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/employees/work-info/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "department_id": "string",
  "job_position_id": "string",
  "job_role_id": "string",
  "reporting_manager_id": "string",
  "shift_id": "string",
  "work_type_id": "string",
  "employee_type_id": "string",
  "location": "string",
  "company_id": "string",
  "email": "string",
  "mobile": "string",
  "date_joining": "string",
  "contract_end_date": "string",
  "basic_salary": "string",
  "salary_hour": "string",
  "additional_info": "string",
  "experience": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/employees/work-info/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/employees/work-info/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/employees/bank-details`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employees/bank-details \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/employees/bank-details`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "bank_name": "string",
  "account_number": "string",
  "branch": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "any_other_code1": "string",
  "any_other_code2": "string",
  "additional_info": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employees/bank-details \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "bank_name": "string",
  "account_number": "string",
  "branch": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "any_other_code1": "string",
  "any_other_code2": "string",
  "additional_info": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/employees/bank-details/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employees/bank-details/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "bank_name": "string",
  "account_number": "string",
  "branch": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "any_other_code1": "string",
  "any_other_code2": "string",
  "additional_info": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/employees/bank-details/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "bank_name": "string",
  "account_number": "string",
  "branch": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "any_other_code1": "string",
  "any_other_code2": "string",
  "additional_info": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/employees/bank-details/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "bank_name": "string",
  "account_number": "string",
  "branch": "string",
  "address": "string",
  "country": "string",
  "state": "string",
  "city": "string",
  "any_other_code1": "string",
  "any_other_code2": "string",
  "additional_info": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/employees/bank-details/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/employees/bank-details/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/accessibility`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/accessibility \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/accessibility`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "feature": "string",
  "filter": "string",
  "exclude_all": "boolean",
  "is_enabled": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/accessibility \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "feature": "string",
  "filter": "string",
  "exclude_all": "boolean",
  "is_enabled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/accessibility/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/accessibility/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "feature": "string",
  "filter": "string",
  "exclude_all": "boolean",
  "is_enabled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/accessibility/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "feature": "string",
  "filter": "string",
  "exclude_all": "string",
  "is_enabled": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/accessibility/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "feature": "string",
  "filter": "string",
  "exclude_all": "boolean",
  "is_enabled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/accessibility/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/accessibility/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/ldap`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/ldap \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/ldap`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "ldap_server": "string",
  "bind_dn": "string",
  "bind_password": "string",
  "base_dn": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/ldap \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "ldap_server": "string",
  "bind_dn": "string",
  "base_dn": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/ldap/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/ldap/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "ldap_server": "string",
  "bind_dn": "string",
  "base_dn": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/ldap/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "ldap_server": "string",
  "bind_dn": "string",
  "bind_password": "string",
  "base_dn": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/ldap/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "ldap_server": "string",
  "bind_dn": "string",
  "base_dn": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/ldap/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/ldap/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/outlook`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/outlook \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/outlook`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "outlook_client_id": "string",
  "outlook_client_secret": "string",
  "outlook_tenant_id": "string",
  "outlook_email": "string",
  "outlook_display_name": "string",
  "outlook_redirect_uri": "string",
  "company_id": "string",
  "is_primary": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/outlook \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "outlook_client_id": "string",
  "outlook_tenant_id": "string",
  "outlook_email": "string",
  "outlook_display_name": "string",
  "company_id": "string",
  "is_primary": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/outlook/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/outlook/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "outlook_client_id": "string",
  "outlook_tenant_id": "string",
  "outlook_email": "string",
  "outlook_display_name": "string",
  "company_id": "string",
  "is_primary": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/outlook/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "outlook_client_id": "string",
  "outlook_client_secret": "string",
  "outlook_tenant_id": "string",
  "outlook_email": "string",
  "outlook_display_name": "string",
  "outlook_redirect_uri": "string",
  "company_id": "string",
  "is_primary": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/outlook/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "outlook_client_id": "string",
  "outlook_tenant_id": "string",
  "outlook_email": "string",
  "outlook_display_name": "string",
  "company_id": "string",
  "is_primary": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/outlook/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/outlook/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/notes`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/notes \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/notes`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "description": "string",
  "updated_by_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/notes \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "integer",
  "description": "string",
  "updated_by_id": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/notes/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/notes/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "integer",
  "description": "string",
  "updated_by_id": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/notes/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "description": "string",
  "updated_by_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/notes/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "integer",
  "description": "string",
  "updated_by_id": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/notes/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/notes/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/tags`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/tags \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/tags`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "color": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/tags \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "color": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/tags/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/tags/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "color": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/tags/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "title": "string",
  "color": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/tags/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "color": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/tags/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/tags/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/action-types`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/action-types \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/action-types`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "action_type": "string",
  "block_option": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/action-types \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "action_type": "string",
  "block_option": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/action-types/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/action-types/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "action_type": "string",
  "block_option": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/action-types/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "title": "string",
  "action_type": "string",
  "block_option": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/action-types/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "action_type": "string",
  "block_option": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/action-types/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/action-types/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/disciplinary-actions`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/disciplinary-actions \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/disciplinary-actions`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "action_id": "integer",
  "description": "string",
  "unit_in": "string",
  "days": "string",
  "hours": "string",
  "start_date": "string",
  "attachment": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/disciplinary-actions \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "integer",
  "action_id": "integer",
  "description": "string",
  "unit_in": "string",
  "days": "string",
  "hours": "string",
  "start_date": "string",
  "attachment": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/disciplinary-actions/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/disciplinary-actions/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "integer",
  "action_id": "integer",
  "description": "string",
  "unit_in": "string",
  "days": "string",
  "hours": "string",
  "start_date": "string",
  "attachment": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/disciplinary-actions/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "employee_id": "string",
  "action_id": "string",
  "description": "string",
  "unit_in": "string",
  "days": "string",
  "hours": "string",
  "start_date": "string",
  "attachment": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/disciplinary-actions/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "integer",
  "action_id": "integer",
  "description": "string",
  "unit_in": "string",
  "days": "string",
  "hours": "string",
  "start_date": "string",
  "attachment": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/disciplinary-actions/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/disciplinary-actions/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/bonus-points`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/bonus-points \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/bonus-points`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "string",
  "points": "integer",
  "encashment_condition": "string",
  "redeeming_points": "string",
  "reason": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/bonus-points \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "points": "integer",
  "encashment_condition": "string",
  "redeeming_points": "string",
  "reason": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/bonus-points/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/bonus-points/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "points": "integer",
  "encashment_condition": "string",
  "redeeming_points": "string",
  "reason": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/bonus-points/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "employee_id": "string",
  "points": "string",
  "encashment_condition": "string",
  "redeeming_points": "string",
  "reason": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/bonus-points/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "employee_id": "string",
  "points": "integer",
  "encashment_condition": "string",
  "redeeming_points": "string",
  "reason": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/bonus-points/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/bonus-points/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/policies`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/policies \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/policies`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "body": "string",
  "is_visible_to_all": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/policies \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "body": "string",
  "is_visible_to_all": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/policies/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/policies/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "body": "string",
  "is_visible_to_all": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/policies/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "title": "string",
  "body": "string",
  "is_visible_to_all": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/policies/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "title": "string",
  "body": "string",
  "is_visible_to_all": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/policies/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/policies/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/general-settings`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/general-settings \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/general-settings`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "badge_id_prefix": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/general-settings \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "badge_id_prefix": "string",
  "company_id": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/general-settings/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/general-settings/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "badge_id_prefix": "string",
  "company_id": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/general-settings/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "badge_id_prefix": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/general-settings/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "created_at": "string",
  "updated_at": "string",
  "id": "integer",
  "badge_id_prefix": "string",
  "company_id": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/general-settings/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/general-settings/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/profile-edit-features`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/profile-edit-features \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "items": [array],
  "total": "integer",
  "page": "integer",
  "page_size": "integer",
  "pages": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Create Item

**POST** `/api/v1/profile-edit-features`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "is_enabled": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/profile-edit-features \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "is_enabled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/profile-edit-features/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/profile-edit-features/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "is_enabled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/profile-edit-features/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "is_enabled": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/profile-edit-features/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "is_enabled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/profile-edit-features/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/profile-edit-features/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### Health

**GET** `/health`

**Description:** No description provided.

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/health \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

