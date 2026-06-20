"""HTTP clients for microservice communication."""

import httpx
from django.conf import settings


class BaseAPIClient:
    service_url: str = ""

    def __init__(self, token: str | None = None):
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _client(self) -> httpx.Client:
        return httpx.Client(base_url=self.service_url, headers=self.headers, timeout=30.0)

    def get(self, path: str, params: dict | None = None) -> dict | list:
        with self._client() as client:
            response = client.get(path, params=params)
            response.raise_for_status()
            return response.json()

    def post(self, path: str, data: dict) -> dict:
        with self._client() as client:
            response = client.post(path, json=data)
            response.raise_for_status()
            return response.json()

    def put(self, path: str, data: dict) -> dict:
        with self._client() as client:
            response = client.put(path, json=data)
            response.raise_for_status()
            return response.json()

    def delete(self, path: str) -> None:
        with self._client() as client:
            response = client.delete(path)
            response.raise_for_status()


class IdentityClient(BaseAPIClient):
    service_url = settings.IDENTITY_SERVICE_URL + "/api/v1"

    def login(self, username: str, password: str) -> dict:
        with httpx.Client(base_url=self.service_url, timeout=30.0) as client:
            response = client.post("/auth/login", json={"username": username, "password": password})
            response.raise_for_status()
            return response.json()

    def list_employees(self, page: int = 1, page_size: int = 50) -> dict:
        return self.get("/employees", params={"page": page, "page_size": page_size})

    def get_employee(self, employee_id: int) -> dict:
        return self.get(f"/employees/{employee_id}")

    def create_employee(self, data: dict) -> dict:
        return self.post("/employees", data)

    def update_employee(self, employee_id: int, data: dict) -> dict:
        return self.put(f"/employees/{employee_id}", data)

    def delete_employee(self, employee_id: int) -> None:
        self.delete(f"/employees/{employee_id}")

    def list_work_info(self) -> dict:
        return self.get("/employees/work-info")

    def create_work_info(self, data: dict) -> dict:
        return self.post("/employees/work-info", data)

    def get_work_info(self, item_id: int) -> dict:
        return self.get(f"/employees/work-info/{item_id}")

    def update_work_info(self, item_id: int, data: dict) -> dict:
        return self.put(f"/employees/work-info/{item_id}", data)

    def delete_work_info(self, item_id: int) -> None:
        self.delete(f"/employees/work-info/{item_id}")

    def list_bank_details(self) -> dict:
        return self.get("/employees/bank-details")

    def create_bank_details(self, data: dict) -> dict:
        return self.post("/employees/bank-details", data)

    def get_bank_details(self, item_id: int) -> dict:
        return self.get(f"/employees/bank-details/{item_id}")

    def update_bank_details(self, item_id: int, data: dict) -> dict:
        return self.put(f"/employees/bank-details/{item_id}", data)

    def delete_bank_details(self, item_id: int) -> None:
        self.delete(f"/employees/bank-details/{item_id}")

    def me(self) -> dict:
        return self.get("/auth/me")


class CoreClient(BaseAPIClient):
    service_url = settings.CORE_SERVICE_URL + "/api/v1"

    def list_companies(self, page: int = 1) -> dict:
        return self.get("/companies", params={"page": page})

    def list_departments(self, page: int = 1) -> dict:
        return self.get("/departments", params={"page": page})

    def list_holidays(self, page: int = 1) -> dict:
        return self.get("/holidays", params={"page": page})


class AttendanceClient(BaseAPIClient):
    service_url = settings.ATTENDANCE_SERVICE_URL + "/api/v1"

    def list_attendance(self, page: int = 1) -> dict:
        return self.get("/attendance", params={"page": page})

    def list_leave_requests(self, page: int = 1) -> dict:
        return self.get("/leave-requests", params={"page": page})

    def list_leave_types(self) -> dict:
        return self.get("/leave-types")


class PayrollClient(BaseAPIClient):
    service_url = settings.PAYROLL_SERVICE_URL + "/api/v1"

    def list_payslips(self, page: int = 1) -> dict:
        return self.get("/payslips", params={"page": page})

    def list_contracts(self, page: int = 1) -> dict:
        return self.get("/contracts", params={"page": page})


class TalentClient(BaseAPIClient):
    service_url = settings.TALENT_SERVICE_URL + "/api/v1"

    def list_recruitment(self, page: int = 1) -> dict:
        return self.get("/recruitment", params={"page": page})

    def list_candidates(self, page: int = 1) -> dict:
        return self.get("/candidates", params={"page": page})

    def list_objectives(self, page: int = 1) -> dict:
        return self.get("/objectives", params={"page": page})

    def list_offboarding(self, page: int = 1) -> dict:
        return self.get("/offboarding", params={"page": page})


class PlatformClient(BaseAPIClient):
    service_url = settings.PLATFORM_SERVICE_URL + "/api/v1"

    def list_notifications(self, page: int = 1) -> dict:
        return self.get("/notifications", params={"page": page})

    def list_documents(self, page: int = 1) -> dict:
        return self.get("/documents", params={"page": page})


class PermissionClient(BaseAPIClient):
    service_url = settings.PERMISSION_SERVICE_URL + "/api/v1"

    def list_roles(self) -> list:
        return self.get("/roles")

    def list_permissions(self) -> list:
        return self.get("/permissions")

    def check_permission(self, codename: str, user_id: int | None = None) -> bool:
        result = self.post("/permissions/check", {"codename": codename, "user_id": user_id})
        return result.get("allowed", False)
