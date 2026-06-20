# Horilla HRMS — Microservices Architecture

Production-ready microservices conversion of the Horilla Django monolith (`horilla-hr/`) into 7 FastAPI services + 1 Django BFF UI layer.

## Architecture

```
                    ┌─────────────┐
                    │   Nginx     │  :80 (API Gateway)
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌──────────────────┐
    │ UI Service  │ │  Identity   │ │  Core / Attendance│ ...
    │ Django BFF  │ │  :8001      │ │  Payroll / etc.   │
    │   :8000     │ └──────┬──────┘ └────────┬─────────┘
    └──────┬──────┘        │                  │
           │               └────────┬─────────┘
           │                        ▼
           │              ┌─────────────────┐
           └─────────────►│   PostgreSQL    │  (7 databases)
                          └─────────────────┘
                                   │
                          ┌────────┴────────┐
                          │  Redis + Celery │
                          └─────────────────┘
```

## Services

| Service | Port | Domain |
|---------|------|--------|
| **horilla-ui-service** | 8000 | Django BFF — renders monolith HTML templates, calls APIs via httpx |
| **horilla-identity-service** | 8001 | Employee, Auth, LDAP, Outlook, Accessibility |
| **horilla-core-service** | 8002 | Company, Department, JobPosition, WorkType, Shift, Holidays, Approvals |
| **horilla-attendance-service** | 8003 | Attendance, Leave, Biometric, Geofencing, FaceDetection |
| **horilla-payroll-service** | 8004 | Payroll, Allowance, Deduction, Contract, Tax, Loan |
| **horilla-permission-service** | 8005 | RBAC: Roles, Permissions, User-Role mapping |
| **horilla-talent-service** | 8006 | Recruitment, PMS, Onboarding, Offboarding |
| **horilla-platform-service** | 8007 | Automations, Notifications, Reports, Audit, Documents |

## Shared Library

`horilla-common-lib/` provides:
- `HorillaBaseMixin` — mirrors Django `HorillaModel` audit fields
- JWT helpers (access + refresh tokens with `is_superuser` flag)
- Permission check via permission service HTTP call
- Celery app factory with retry logic (max_retries=3, exponential backoff)
- Event publishing (`employee.created`, `department.deleted`)
- Generic CRUD router factory
- Email Jinja2 templates

## Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start all services (development with hot reload)
docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

# 3. Access
# UI:        http://localhost:8000
# Nginx:     http://localhost
# Identity:  http://localhost:8001/docs
# Core:      http://localhost:8002/docs
# ... (each service has /docs and /redoc)
```

## API Gateway Routes (Nginx)

| Path | Service |
|------|---------|
| `/` | UI BFF |
| `/api/identity/*` | Identity Service |
| `/api/core/*` | Core Service |
| `/api/attendance/*` | Attendance Service |
| `/api/payroll/*` | Payroll Service |
| `/api/permission/*` | Permission Service |
| `/api/talent/*` | Talent Service |
| `/api/platform/*` | Platform Service |

## Authentication

All FastAPI services use JWT Bearer tokens:

```bash
# Login
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Use token
curl http://localhost:8001/api/v1/employees \
  -H "Authorization: Bearer <access_token>"
```

JWT payload includes: `user_id`, `employee_id`, `is_superuser`, `is_staff`.

## RBAC (Permission Service)

On startup, the permission service auto-seeds:

**Modules:** Base, Employee, Attendance, Leave, Payroll, Recruitment, PMS, Onboarding, Offboarding, Asset, Project, Helpdesk

**Actions:** view, add, change, delete

**Default Roles:** Admin (all permissions), Manager (view/add/change), Employee (view)

Permission check endpoint: `POST /api/v1/permissions/check`

## Event Flow (Celery + Redis)

| Event | Publisher | Subscribers |
|-------|-----------|-------------|
| `employee.created` | Identity Service | Attendance, Payroll workers |
| `department.deleted` | Core Service | Identity worker (unassign employees) |

All Celery tasks use `max_retries=3` with exponential backoff.

## UI BFF (Django)

The UI service:
- Mounts monolith `templates/` and `static/` from `horilla-hr/`
- Does **not** connect to any database directly
- Stores JWT in session after login
- Passes `Authorization: Bearer` header to all microservice calls via `httpx` clients in `clients/api_clients.py`

## Environment Variables

See `.env.example` for the full list. Key variables:

| Variable | Description |
|----------|-------------|
| `JWT_SECRET_KEY` | Shared secret for all services |
| `POSTGRES_USER/PASSWORD` | PostgreSQL credentials |
| `REDIS_URL` | Redis broker URL |
| `CELERY_BROKER_URL` | Celery message broker |
| `IDENTITY_DATABASE_URL` | Per-service async PostgreSQL URL |
| `IDENTITY_SERVICE_URL` | Internal Docker service URL for BFF |

## Endpoint Summary

### Identity Service (`/api/v1`)
- `POST /auth/login`, `/auth/refresh`, `/auth/register`, `GET /auth/me`
- `CRUD /employees`, `/employees/work-info`, `/employees/bank-details`
- `CRUD /accessibility`, `/ldap`, `/outlook`

### Core Service (`/api/v1`)
- `CRUD /companies`, `/departments`, `/job-positions`, `/job-roles`
- `CRUD /work-types`, `/employee-types`, `/shifts`, `/holidays`
- `CRUD /work-type-requests`, `/shift-requests`, `/approval-conditions`

### Attendance Service (`/api/v1`)
- `CRUD /attendance`, `/leave-types`, `/leave-requests`
- `CRUD /biometric-devices`, `/geofencing`

### Payroll Service (`/api/v1`)
- `CRUD /contracts`, `/allowances`, `/deductions`, `/payslips`, `/loans`

### Permission Service (`/api/v1`)
- `GET /permissions`, `POST /permissions/check`
- `GET/POST /roles`, `POST /user-roles`

### Talent Service (`/api/v1`)
- `CRUD /recruitment`, `/candidates`, `/objectives`, `/employee-objectives`
- `CRUD /feedback`, `/offboarding`, `/resignation-letters`

### Platform Service (`/api/v1`)
- `CRUD /automations`, `/notifications`, `/document-requests`, `/documents`

## Development

```bash
# Run a single service locally
cd horilla-identity-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Run Celery worker
celery -A app.celery_worker.celery_app worker --loglevel=info
```

## Project Structure

```
Horilla-HRMS/
├── horilla-common-lib/          # Shared library
├── horilla-identity-service/    # Port 8001
├── horilla-core-service/        # Port 8002
├── horilla-attendance-service/  # Port 8003
├── horilla-payroll-service/     # Port 8004
├── horilla-permission-service/  # Port 8005
├── horilla-talent-service/      # Port 8006
├── horilla-platform-service/    # Port 8007
├── horilla-ui-service/          # Port 8000 (Django BFF)
├── horilla-hr/                  # Original Django monolith (source of truth)
├── nginx/nginx.conf
├── docker-compose.yml
├── docker-compose.override.yml
├── scripts/init-databases.sh
└── .env.example
```

## Models

All SQLAlchemy models mirror the Django monolith field-for-field. Cross-service references use integer IDs (e.g., `department_id`, `company_id`) rather than foreign keys across databases, following microservices best practices.

## License

Same as Horilla HRMS monolith.
