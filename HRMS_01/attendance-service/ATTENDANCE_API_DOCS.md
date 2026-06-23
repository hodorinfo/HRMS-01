# Attendance Service API Documentation

Complete API reference for Attendance Service.

**Service:** Attendance Service  
**Port:** 8000 (Internal) / 8003 (Mapped)  
**Base URL (Direct):** `http://localhost:8003`  
**Base URL (Gateway):** `http://192.168.1.41` (via Nginx)  
**Container:** `hrms_01-attendance-service-1`

**Authentication:** JWT Bearer Token (all API endpoints except health)  
**Schema:** `horilla_attendance` (PostgreSQL)

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


### List Items

**GET** `/api/v1/attendance`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/attendance \
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

**POST** `/api/v1/attendance`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "attendance_date": "string",
  "shift_id": "string",
  "work_type_id": "string",
  "attendance_clock_in_date": "string",
  "attendance_clock_in": "string",
  "attendance_clock_out_date": "string",
  "attendance_clock_out": "string",
  "minimum_hour": "string",
  "is_holiday": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/attendance \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "attendance_date": "string",
  "shift_id": "string",
  "attendance_clock_in": "string",
  "attendance_clock_out": "string",
  "attendance_worked_hour": "string",
  "attendance_validated": "boolean",
  "is_holiday": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/attendance/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/attendance/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "attendance_date": "string",
  "shift_id": "string",
  "attendance_clock_in": "string",
  "attendance_clock_out": "string",
  "attendance_worked_hour": "string",
  "attendance_validated": "boolean",
  "is_holiday": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/attendance/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "shift_id": "string",
  "attendance_clock_in": "string",
  "attendance_clock_out": "string",
  "attendance_validated": "string",
  "attendance_overtime_approve": "string",
  "request_description": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/attendance/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "attendance_date": "string",
  "shift_id": "string",
  "attendance_clock_in": "string",
  "attendance_clock_out": "string",
  "attendance_worked_hour": "string",
  "attendance_validated": "boolean",
  "is_holiday": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/attendance/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/attendance/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/leave-types`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/leave-types \
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

**POST** `/api/v1/leave-types`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "name": "string",
  "color": "string",
  "payment": "string",
  "count": "number",
  "period_in": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/leave-types \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "name": "string",
  "color": "string",
  "payment": "string",
  "count": "number",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/leave-types/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/leave-types/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "name": "string",
  "color": "string",
  "payment": "string",
  "count": "number",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/leave-types/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "name": "string",
  "color": "string",
  "count": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/leave-types/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "name": "string",
  "color": "string",
  "payment": "string",
  "count": "number",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/leave-types/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/leave-types/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/leave-requests`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/leave-requests \
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

**POST** `/api/v1/leave-requests`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "leave_type_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "requested_days": "number",
  "description": "string",
  "start_date_breakdown": "string",
  "end_date_breakdown": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/leave-requests \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "leave_type_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "requested_days": "number",
  "status": "string",
  "description": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/leave-requests/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/leave-requests/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "leave_type_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "requested_days": "number",
  "status": "string",
  "description": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/leave-requests/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "status": "string",
  "reject_reason": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/leave-requests/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "leave_type_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "requested_days": "number",
  "status": "string",
  "description": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/leave-requests/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/leave-requests/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/biometric-devices`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/biometric-devices \
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

**POST** `/api/v1/biometric-devices`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "name": "string",
  "machine_type": "string",
  "machine_ip": "string",
  "port": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/biometric-devices \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "string",
  "name": "string",
  "machine_type": "string",
  "is_live": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/biometric-devices/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/biometric-devices/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "string",
  "name": "string",
  "machine_type": "string",
  "is_live": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/biometric-devices/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "name": "string",
  "machine_type": "string",
  "machine_ip": "string",
  "port": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/biometric-devices/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "string",
  "name": "string",
  "machine_type": "string",
  "is_live": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/biometric-devices/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/biometric-devices/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/geofencing`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/geofencing \
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

**POST** `/api/v1/geofencing`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "latitude": "number",
  "longitude": "number",
  "radius_in_meters": "integer",
  "company_id": "string",
  "start": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/geofencing \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "latitude": "number",
  "longitude": "number",
  "radius_in_meters": "integer",
  "start": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/geofencing/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/geofencing/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "latitude": "number",
  "longitude": "number",
  "radius_in_meters": "integer",
  "start": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/geofencing/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "latitude": "number",
  "longitude": "number",
  "radius_in_meters": "integer",
  "company_id": "string",
  "start": "boolean",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/geofencing/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "latitude": "number",
  "longitude": "number",
  "radius_in_meters": "integer",
  "start": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/geofencing/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/geofencing/{item_id} \
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

