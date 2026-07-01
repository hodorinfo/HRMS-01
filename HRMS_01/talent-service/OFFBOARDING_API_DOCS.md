# Offboarding API Documentation

Complete API reference for the Offboarding module (part of Talent Service).

**Service:** Talent Service  
**Port:** 8000 (Internal) / 8006 (Mapped)  
**Base URL (Direct):** `http://localhost:8006`  
**Base URL (Gateway):** `http://192.168.1.41` (via Nginx)  
**Container:** `hrms_01-talent-service-1`

**Authentication:** JWT Bearer Token (all API endpoints except health)  
**Schema:** `horilla_talent` (PostgreSQL)

---

## Endpoints

### List Items

**GET** `/api/v1/offboarding`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding \
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

**POST** `/api/v1/offboarding`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "description": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/offboarding \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/offboarding/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/offboarding/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "title": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/offboarding/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/offboarding/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/offboarding/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/offboarding-stages`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding-stages \
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

**POST** `/api/v1/offboarding-stages`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "type": "string",
  "offboarding_id": "integer",
  "sequence": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/offboarding-stages \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "offboarding_id": "integer",
  "sequence": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/offboarding-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "offboarding_id": "integer",
  "sequence": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/offboarding-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "offboarding_id": "integer",
  "sequence": "integer",
  "is_active": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/offboarding-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "offboarding_id": "integer",
  "sequence": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/offboarding-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/offboarding-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/offboarding-employees`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding-employees \
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

**POST** `/api/v1/offboarding-employees`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "stage_id": "integer",
  "notice_period": "integer",
  "unit": "string",
  "notice_period_starts": "string",
  "notice_period_ends": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/offboarding-employees \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "stage_id": "integer",
  "notice_period": "integer",
  "unit": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/offboarding-employees/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding-employees/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "stage_id": "integer",
  "notice_period": "integer",
  "unit": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/offboarding-employees/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "stage_id": "integer",
  "notice_period": "integer",
  "unit": "string",
  "is_active": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/offboarding-employees/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "stage_id": "integer",
  "notice_period": "integer",
  "unit": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/offboarding-employees/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/offboarding-employees/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/offboarding-tasks`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding-tasks \
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

**POST** `/api/v1/offboarding-tasks`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "stage_id": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/offboarding-tasks \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "stage_id": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/offboarding-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/offboarding-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "stage_id": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/offboarding-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "title": "string",
  "stage_id": "integer",
  "is_active": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/offboarding-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "stage_id": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/offboarding-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/offboarding-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/employee-tasks`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employee-tasks \
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

**POST** `/api/v1/employee-tasks`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "status": "string",
  "task_id": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/employee-tasks \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "status": "string",
  "task_id": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/employee-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/employee-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "status": "string",
  "task_id": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/employee-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "status": "string",
  "task_id": "integer",
  "is_active": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/employee-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "status": "string",
  "task_id": "integer",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/employee-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/employee-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/resignation-letters`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/resignation-letters \
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

**POST** `/api/v1/resignation-letters`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "title": "string",
  "description": "string",
  "planned_to_leave_on": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/resignation-letters \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "title": "string",
  "planned_to_leave_on": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/resignation-letters/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/resignation-letters/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "title": "string",
  "planned_to_leave_on": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/resignation-letters/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "title": "string",
  "planned_to_leave_on": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/resignation-letters/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "title": "string",
  "planned_to_leave_on": "string",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/resignation-letters/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/resignation-letters/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


#functional Requirement:



### 1. Offboarding Pipeline Configuration
* **Offboarding Definition:** HR administrators can create customized offboarding pipelines (e.g., standard offboarding, immediate termination) with titles and descriptions.
* **Stage Management:** The system automatically initializes standard offboarding stages (e.g., Notice Period, Exit Interview, Work Handover, FnF Settlement, Farewell, Archived) for every new pipeline.
* **Task Definitions:** HR managers can define specific tasks within each offboarding stage (e.g., "Return Laptop" in the Work Handover stage, "Clear Dues" in FnF).
* **Manager Assignment:** Pipelines, stages, and tasks can all have designated managers (employees) assigned to oversee their execution.

### 2. Resignation Management
* **Employee Requests:** Employees must be able to submit formal resignation requests specifying a title, description, and their proposed `planned_to_leave_on` date.
* **Approval Workflow:** Managers can review these requests and mark them as `requested`, `approved`, or `rejected`.
* **Automatic Transition:** Upon approval of a resignation request, the system must support smoothly transitioning the employee into the active offboarding pipeline.

### 3. Employee Offboarding Tracking
* **Notice Period Calculation:** The system tracks the employee's notice period duration, automatically recording the `notice_period_starts` and calculating the `notice_period_ends` based on company policy settings.
* **Exit Interviews & Reasons:** HR must be able to document the official `ExitReason`, including descriptions and supporting file attachments.
* **Stage Tracking:** The system tracks which specific stage an offboarding employee is currently progressing through.
* **HR Notes:** Managers or HR personnel can add miscellaneous notes (and attachments) tied to specific employees and offboarding stages.

### 4. Employee Task Execution
* **Task Assignment:** Specific offboarding tasks are assigned to the exiting employee (or their managers).
* **Status Tracking:** The lifecycle of each task is tracked through statuses: `todo`, `in_progress`, `stuck`, and `completed`.
* **Audit & Notifications:** The system maintains an audit log (history) of task status changes. It also automatically dispatches in-app notifications to employees when an offboarding task is assigned to them.




