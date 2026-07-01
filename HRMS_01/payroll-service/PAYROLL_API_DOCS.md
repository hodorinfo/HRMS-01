# Payroll Service API Documentation

Complete API reference for Payroll Service.

**Service:** Payroll Service  
**Port:** 8000 (Internal) / 8004 (Mapped)  
**Base URL (Direct):** `http://localhost:8004`  
**Base URL (Gateway):** `http://192.168.1.41` (via Nginx)  
**Container:** `hrms_01-payroll-service-1`

**Authentication:** JWT Bearer Token (all API endpoints except health)  
**Schema:** `horilla_payroll` (PostgreSQL)

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

**GET** `/api/v1/contracts`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/contracts \
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

**POST** `/api/v1/contracts`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "contract_name": "string",
  "employee_id": "integer",
  "contract_start_date": "string",
  "contract_end_date": "string",
  "wage_type": "string",
  "pay_frequency": "string",
  "wage": "number",
  "filing_status_id": "string",
  "contract_status": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/contracts \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "contract_name": "string",
  "employee_id": "integer",
  "contract_start_date": "string",
  "wage_type": "string",
  "pay_frequency": "string",
  "wage": "number",
  "contract_status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/contracts/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/contracts/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "contract_name": "string",
  "employee_id": "integer",
  "contract_start_date": "string",
  "wage_type": "string",
  "pay_frequency": "string",
  "wage": "number",
  "contract_status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/contracts/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "contract_name": "string",
  "contract_end_date": "string",
  "wage": "string",
  "contract_status": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/contracts/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "contract_name": "string",
  "employee_id": "integer",
  "contract_start_date": "string",
  "wage_type": "string",
  "pay_frequency": "string",
  "wage": "number",
  "contract_status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/contracts/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/contracts/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/allowances`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/allowances \
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

**POST** `/api/v1/allowances`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "amount": "number",
  "is_taxable": "boolean",
  "is_fixed": "boolean",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/allowances \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "amount": "number",
  "is_taxable": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/allowances/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/allowances/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "amount": "number",
  "is_taxable": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/allowances/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "title": "string",
  "amount": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/allowances/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "amount": "number",
  "is_taxable": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/allowances/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/allowances/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/deductions`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/deductions \
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

**POST** `/api/v1/deductions`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "amount": "number",
  "is_tax": "boolean",
  "is_fixed": "boolean",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/deductions \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "amount": "number",
  "is_tax": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/deductions/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/deductions/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "amount": "number",
  "is_tax": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/deductions/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "title": "string",
  "amount": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/deductions/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "amount": "number",
  "is_tax": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/deductions/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/deductions/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/payslips`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/payslips \
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

**POST** `/api/v1/payslips`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "employee_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "contract_wage": "number",
  "basic_pay": "number",
  "gross_pay": "number",
  "deduction": "number",
  "net_pay": "number",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/payslips \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "gross_pay": "number",
  "net_pay": "number",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/payslips/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/payslips/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "gross_pay": "number",
  "net_pay": "number",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/payslips/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "status": "string",
  "sent_to_employee": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/payslips/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "employee_id": "integer",
  "start_date": "string",
  "end_date": "string",
  "gross_pay": "number",
  "net_pay": "number",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/payslips/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/payslips/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/loans`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/loans \
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

**POST** `/api/v1/loans`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "type": "string",
  "title": "string",
  "employee_id": "integer",
  "loan_amount": "number",
  "provided_date": "string",
  "installment_amount": "number",
  "installments": "integer",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/loans \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "type": "string",
  "title": "string",
  "employee_id": "integer",
  "loan_amount": "number",
  "settled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/loans/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/loans/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "type": "string",
  "title": "string",
  "employee_id": "integer",
  "loan_amount": "number",
  "settled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/loans/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "type": "string",
  "title": "string",
  "employee_id": "integer",
  "loan_amount": "number",
  "provided_date": "string",
  "installment_amount": "number",
  "installments": "integer",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/loans/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "type": "string",
  "title": "string",
  "employee_id": "integer",
  "loan_amount": "number",
  "settled": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/loans/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/loans/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/filing-status`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/filing-status \
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

**POST** `/api/v1/filing-status`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "filing_status": "string",
  "based_on": "string",
  "use_py": "boolean",
  "python_code": "string",
  "description": "string",
  "company_id": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/filing-status \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "filing_status": "string",
  "based_on": "string",
  "use_py": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/filing-status/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/filing-status/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "filing_status": "string",
  "based_on": "string",
  "use_py": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/filing-status/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "filing_status": "string",
  "based_on": "string",
  "use_py": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/filing-status/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "filing_status": "string",
  "based_on": "string",
  "use_py": "boolean",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/filing-status/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/filing-status/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### List Items

**GET** `/api/v1/reimbursements`

**Description:** No description provided.

**Query Parameters:**
- `page` (integer)
- `page_size` (integer)

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/reimbursements \
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

**POST** `/api/v1/reimbursements`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "title": "string",
  "type": "string",
  "employee_id": "integer",
  "amount": "number",
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/reimbursements \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "employee_id": "integer",
  "amount": "number",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Get Item

**GET** `/api/v1/reimbursements/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/reimbursements/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "employee_id": "integer",
  "amount": "number",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Update Item

**PUT** `/api/v1/reimbursements/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "status": "string",
  "amount": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/reimbursements/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{
  "id": "integer",
  "title": "string",
  "type": "string",
  "employee_id": "integer",
  "amount": "number",
  "status": "string",
  "is_active": "boolean",
}
```

**Error Responses:**
- `422`: Validation Error


### Delete Item

**DELETE** `/api/v1/reimbursements/{item_id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X DELETE http://192.168.1.41/api/v1/reimbursements/{item_id} \
  -H "Authorization: Bearer <token>"
```

**Response:** Standard Success Response

**Error Responses:**
- `422`: Validation Error


### Download Payslip

**GET** `/api/v1/payslip-download/{id}`

**Description:** No description provided.

**Query Parameters:**

**Request (Gateway):**
```bash
curl -X GET http://192.168.1.41/api/v1/payslip-download/{id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Send Payslip Mail

**POST** `/api/v1/payslip-send-mail/`

**Description:** No description provided.

**Request Body Example:**
```json
{
  "payslip_id": "integer",
  "email": "string",
}
```

**Request (Gateway):**
```bash
curl -X POST http://192.168.1.41/api/v1/payslip-send-mail/ \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Approve Reject Reimbursement

**PUT** `/api/v1/reimbursement-approve-reject/{id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/reimbursement-approve-reject/{id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

**Error Responses:**
- `422`: Validation Error


### Approve Reject Reimbursement

**PUT** `/api/v1/reimbusement-approve-reject/{id}`

**Description:** No description provided.

**Query Parameters:**

**Request Body Example:**
```json
{
  "status": "string",
}
```

**Request (Gateway):**
```bash
curl -X PUT http://192.168.1.41/api/v1/reimbusement-approve-reject/{id} \
  -H "Authorization: Bearer <token>"
```

**Response Example (Success):**
```json
{}
```

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
`

## Functional Requirements:``

Based on the backend architecture and database models (models.py) of the Horilla HRMS, here are the complete Functional Requirements of the Payroll Module:

1. 📄 Contract Management
Base Salary Configuration: Define the fundamental salary structure for each employee (e.g., Hourly Wage or Monthly Salary).
Contract Lifecycle: Track the start date, end date, and status of an employee's work contract. The contract acts as the base value for all other payroll calculations.


2. ➕ Allowances Management
Dynamic Allowances: Create custom allowances like HRA (House Rent Allowance), Transport Allowance, or Medical Allowance.
Calculation Rules: Allowances can be configured as a Fixed Amount or a Percentage (%) of the basic wage.
Conditional Allowances: Apply allowances conditionally based on attendance, shifts, or specific employee categories.

3. ➖ Deductions & Taxation
Custom Deductions: Manage statutory and company-level deductions like Provident Fund (PF), Health Insurance, or Late-coming penalties.
Federal / Income Tax Rules: Configure tax slabs based on 'Filing Status' (e.g., Single, Married). The system calculates taxable income and applies appropriate tax deductions automatically.
Deduction Types: Like allowances, deductions can also be a flat amount or a percentage of the salary.

4. 💸 Loan & Advance Salary Management
Loan Issuance: HR can issue loans or advance salaries to employees.
EMI Tracking: The system tracks the total loan amount, the amount already paid, and the outstanding balance.
Auto-Deduction: The monthly EMI is automatically calculated and deducted from the employee's monthly payslip until the loan is fully recovered.

5. 🧾 Reimbursements & Leave Encashment
Expense Claims: Employees can submit reimbursement requests for business expenses (travel, meals, etc.) along with file attachments (receipts/bills).
Approval Workflow: Managers/HR can review, approve, or reject these claims. Approved claims are added to the next payslip.
Leave Encashment: Convert unused paid leaves into encashable monetary value at the end of the year or during resignation, based on EncashmentGeneralSettings.

6. 📝 Payslip Generation
Salary Calculation Engine: Automatically calculates Gross Pay (Base + Allowances + Reimbursements) and Net Pay (Gross - Deductions - Loan EMIs).
Automated Generation: System can be configured to automatically generate payslips on a specific date every month (PayslipAutoGenerate).
Export & View: Employees can view their salary breakdown and download their Payslips as PDFs. HR can export bulk payroll data for bank transfers.

7. 📊 Payroll Dashboard
Provides HR and Finance teams with a high-level overview of the total company payroll cost, pending reimbursement approvals, active employee loans, and tax liabilities.
In short: The module acts as a complete pipeline. It takes the Employee's Contract as the base, checks their Attendance/Leaves, adds Allowances/Reimbursements, subtracts Deductions/Loans/Taxes, and finally outputs a ready-to-print Payslip.

11:47 AM


