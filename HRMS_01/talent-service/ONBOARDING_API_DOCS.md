# Talent Service API Documentation

Complete API reference for Talent Service (including Onboarding).

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

**GET** `/api/v1/onboarding-stages`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/onboarding-stages \
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

**POST** `/api/v1/onboarding-stages`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "recruitment_id": "integer",
  "sequence": "integer",
  "is_final_stage": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/onboarding-stages \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "recruitment_id": "integer",
  "sequence": "integer",
  "is_final_stage": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/onboarding-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/onboarding-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "recruitment_id": "integer",
  "sequence": "integer",
  "is_final_stage": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/onboarding-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "recruitment_id": "integer",
  "sequence": "integer",
  "is_final_stage": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/onboarding-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "recruitment_id": "integer",
  "sequence": "integer",
  "is_final_stage": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/onboarding-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/onboarding-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/onboarding-tasks`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/onboarding-tasks \
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

**POST** `/api/v1/onboarding-tasks`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "stage_id": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/onboarding-tasks \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "stage_id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/onboarding-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/onboarding-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "stage_id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/onboarding-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "stage_id": "integer",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/onboarding-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "stage_id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/onboarding-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/onboarding-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/candidate-stages`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidate-stages \
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

**POST** `/api/v1/candidate-stages`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "candidate_id": "integer",
  "onboarding_stage_id": "integer",
  "onboarding_end_date": "string",
  "sequence": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/candidate-stages \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "onboarding_stage_id": "integer",
  "onboarding_end_date": "string",
  "sequence": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/candidate-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidate-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "onboarding_stage_id": "integer",
  "onboarding_end_date": "string",
  "sequence": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/candidate-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "onboarding_stage_id": "integer",
  "onboarding_end_date": "string",
  "sequence": "integer",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/candidate-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "onboarding_stage_id": "integer",
  "onboarding_end_date": "string",
  "sequence": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/candidate-stages/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/candidate-stages/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/candidate-tasks`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidate-tasks \
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

**POST** `/api/v1/candidate-tasks`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "candidate_id": "integer",
  "stage_id": "integer",
  "onboarding_task_id": "integer",
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/candidate-tasks \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "stage_id": "integer",
  "onboarding_task_id": "integer",
  "status": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/candidate-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidate-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "stage_id": "integer",
  "onboarding_task_id": "integer",
  "status": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/candidate-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "stage_id": "integer",
  "onboarding_task_id": "integer",
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/candidate-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "stage_id": "integer",
  "onboarding_task_id": "integer",
  "status": "string",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/candidate-tasks/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/candidate-tasks/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/onboarding-portals`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/onboarding-portals \
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

**POST** `/api/v1/onboarding-portals`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "candidate_id": "integer",
  "token": "string",
  "used": "boolean",
  "count": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/onboarding-portals \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "token": "string",
  "used": "boolean",
  "count": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/onboarding-portals/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/onboarding-portals/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "token": "string",
  "used": "boolean",
  "count": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/onboarding-portals/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "token": "string",
  "used": "boolean",
  "count": "integer",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/onboarding-portals/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "candidate_id": "integer",
  "token": "string",
  "used": "boolean",
  "count": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/onboarding-portals/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/onboarding-portals/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/candidates`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidates \
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

**POST** `/api/v1/candidates`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "name": "string",
  "email": "string",
  "resume_url": "string",
  "hiring_request_id": "integer",
  "stage_id": "string",
  "source_channel_id": "string",
  "rejection_reason_id": "string",
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/candidates \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "name": "string",
  "email": "string",
  "resume_url": "string",
  "hiring_request_id": "integer",
  "stage_id": "string",
  "source_channel_id": "string",
  "rejection_reason_id": "string",
  "status": "string",
  "id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/candidates/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidates/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "name": "string",
  "email": "string",
  "resume_url": "string",
  "hiring_request_id": "integer",
  "stage_id": "string",
  "source_channel_id": "string",
  "rejection_reason_id": "string",
  "status": "string",
  "id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/candidates/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "name": "string",
  "email": "string",
  "resume_url": "string",
  "hiring_request_id": "string",
  "stage_id": "string",
  "source_channel_id": "string",
  "rejection_reason_id": "string",
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/candidates/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "name": "string",
  "email": "string",
  "resume_url": "string",
  "hiring_request_id": "integer",
  "stage_id": "string",
  "source_channel_id": "string",
  "rejection_reason_id": "string",
  "status": "string",
  "id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/candidates/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/candidates/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/candidate-screenings`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidate-screenings \
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

**POST** `/api/v1/candidate-screenings`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "candidate_id": "integer",
  "cv_education_consistency": "boolean",
  "cv_type": "string",
  "icp_match_score": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/candidate-screenings \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "candidate_id": "integer",
  "cv_education_consistency": "boolean",
  "cv_type": "string",
  "icp_match_score": "string",
  "id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/candidate-screenings/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/candidate-screenings/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "candidate_id": "integer",
  "cv_education_consistency": "boolean",
  "cv_type": "string",
  "icp_match_score": "string",
  "id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/candidate-screenings/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "candidate_id": "string",
  "cv_education_consistency": "boolean",
  "cv_type": "string",
  "icp_match_score": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/candidate-screenings/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "candidate_id": "integer",
  "cv_education_consistency": "boolean",
  "cv_type": "string",
  "icp_match_score": "string",
  "id": "integer",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/candidate-screenings/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/candidate-screenings/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


# Functional Requirements:



### 1. Onboarding Pipeline Configuration (Stages & Tasks)
* **Stage Management:** HR administrators or managers must be able to define customizable onboarding stages (e.g., "Documentation," "IT Setup," "Orientation") linked to specific recruitment drives.
* **Stage Sequencing:** Stages must have a defined sequence/order, with the ability to mark a specific stage as the "Final Stage."
* **Task Definitions:** Within each stage, managers must be able to create granular onboarding tasks (e.g., "Submit ID," "Setup Laptop").
* **Manager Assignment:** Both stages and individual tasks must be assignable to specific employees (Task/Stage Managers) who are responsible for overseeing them.

### 2. Candidate Onboarding Tracking
* **Candidate Stage Tracking:** The system must track each candidate's progression through the onboarding stages.
* **Task Completion Metrics:** The system must calculate and display a completion ratio for each candidate (e.g., "3/5 tasks completed").
* **Automatic Completion:** When a candidate successfully completes the "Final Stage," the system must automatically record their `onboarding_end_date`.

### 3. Candidate Task Management
* **Status Tracking:** Each onboarding task assigned to a candidate must have a tracked lifecycle. The available statuses are:
  * `Todo`
  * `Scheduled`
  * `Ongoing`
  * `Stuck`
  * `Done`
* **Audit Logging:** Any changes to the status of a candidate's task must be historically logged for auditing purposes.

### 4. Candidate Self-Service Portal
* **Secure Access:** The system must generate a unique token for each candidate to access a dedicated onboarding portal securely without requiring full employee credentials.
* **Token Tracking:** The system must track whether the token has been `used` and the `count` of access attempts.
* **Profile Management:** Candidates must be able to upload initial profile information (like a profile picture) via the portal before officially becoming employees.



