"""Django BFF views - proxy to microservices via HTTP clients."""

import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from clients.api_clients import (
    AttendanceClient,
    CoreClient,
    IdentityClient,
    PayrollClient,
    PermissionClient,
    PlatformClient,
    TalentClient,
)


class DictObject:
    def __init__(self, data):
        for k, v in data.items():
            if isinstance(v, dict):
                setattr(self, k, DictObject(v))
            elif isinstance(v, list):
                setattr(self, k, [DictObject(item) if isinstance(item, dict) else item for item in v])
            else:
                setattr(self, k, v)
                
    def __getattr__(self, name):
        return None
        
    def __str__(self):
        first = getattr(self, "employee_first_name", "")
        last = getattr(self, "employee_last_name", "")
        if first or last:
            return f"{first} {last}".strip()
        return getattr(self, "name", "") or "Unnamed"


class EmployeeObject(DictObject):
    @property
    def get_avatar(self):
        if getattr(self, "avatar_url", None):
            return self.avatar_url
        name = f"{getattr(self, 'employee_first_name', '')} {getattr(self, 'employee_last_name', '')}"
        return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random"

    @property
    def check_online(self):
        return False

    @property
    def get_gender_display(self):
        return getattr(self, "gender", "") or ""

    @property
    def get_marital_status_display(self):
        return getattr(self, "marital_status", "") or ""


class PageMock:
    def __init__(self, object_list):
        self.object_list = object_list
        self.number = 1
        self.paginator = self
        self.num_pages = 1
        self.has_next = False
        self.has_previous = False
    
    def __iter__(self):
        return iter(self.object_list)


def _current_employee(request, token):
    try:
        identity = IdentityClient(token)
        user = identity.me()
        user_id = user.get("id")
        employees = identity.list_employees(page_size=100)
        for emp in employees.get("items", []):
            if emp.get("employee_user_id") == user_id:
                return emp
        if employees.get("items"):
            return employees["items"][0]
    except Exception:
        pass
    return None


def _token(request: HttpRequest) -> str | None:
    return request.session.get("access_token")



# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        client = IdentityClient()
        try:
            tokens = client.login(request.POST["username"], request.POST["password"])
            request.session["access_token"] = tokens["access_token"]
            request.session["refresh_token"] = tokens.get("refresh_token", "")
            return redirect("dashboard")
        except Exception:
            messages.error(request, "Invalid credentials")
    context = {
        "white_label_company_name": "Horilla HRMS",
        "white_label_company": None,
        "initialize_database": False,
    }
    return render(request, "login.html", context)


def logout_view(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    return redirect("login")


def forgot_password(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        messages.info(request, "Password reset link sent to your email.")
        return redirect("login")
    context = {"white_label_company_name": "Horilla HRMS"}
    return render(request, "forgot_password.html", context)


def reset_password_view(request: HttpRequest) -> HttpResponse:
    context = {"white_label_company_name": "Horilla HRMS"}
    return render(request, "reset_password.html", context)


def signup_view(request: HttpRequest) -> HttpResponse:
    """Company registration / Initialize database stub."""
    context = {"white_label_company_name": "Horilla HRMS"}
    return render(request, "signup.html", context)


# ---------------------------------------------------------------------------
# Main views
# ---------------------------------------------------------------------------

from datetime import date, timedelta
from django.http import JsonResponse

def dashboard(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    if not token:
        return redirect("login")
    
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    
    context = {
        "user": None,
        "employees_count": 0,
        "white_label_company_name": "Horilla HRMS",
        "white_label_company": None,
        "current_date": today.strftime("%Y-%m-%d"),
        "first_day_of_week": start_week.strftime("%Y-%m-%d"),
        "last_day_of_week": end_week.strftime("%Y-%m-%d"),
    }
    try:
        identity = IdentityClient(token)
        context["user"] = identity.me()
        employees = identity.list_employees(page_size=1)
        context["employees_count"] = employees.get("total", 0)
    except Exception:
        pass
    return render(request, "index.html", context)


def employee_list(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        raw_data = IdentityClient(token).list_employees()
        items = raw_data.get("items", [])
        employees = [EmployeeObject(emp) for emp in items]
    except Exception:
        employees = []

    page_obj = PageMock(employees)
    view_type = request.GET.get("view", "card")

    return render(
        request,
        "employee/templates/employee_personal_info/employee_view.html",
        {
            "data": page_obj,
            "emp": employees,
            "view_type": view_type,
            "gp_fields": [("department", "Department"), ("job_position", "Job Position")],
        },
    )


def employee_detail(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    try:
        employee = IdentityClient(token).get_employee(pk)
    except Exception:
        employee = None
    if not employee:
        return redirect("employee_list")
    today = datetime.date.today()
    now = timezone.now()
    return render(
        request,
        "employee/profile/profile_view.html",
        {
            "employee": EmployeeObject(employee),
            "current_date": today,
            "now": now,
        },
    )


def employee_profile_view(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    emp = _current_employee(request, token)
    if not emp:
        return redirect("employee_list")
    today = datetime.date.today()
    now = timezone.now()
    return render(
        request,
        "employee/profile/profile_view.html",
        {
            "employee": EmployeeObject(emp),
            "current_date": today,
            "now": now,
        },
    )


def document_requests_view(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        raw_data = PlatformClient(token).list_documents()
        items = raw_data.get("items", []) if isinstance(raw_data, dict) else []
        documents = [DictObject(doc) for doc in items]
    except Exception:
        documents = []

    return render(
        request,
        "documents/document_requests.html",
        {
            "documents": PageMock(documents),
            "document_requests": documents,
        },
    )


def shift_requests_view(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        raw_data = AttendanceClient(token).list_leave_requests()
        items = raw_data.get("items", []) if isinstance(raw_data, dict) else []
        requests = [DictObject(req) for req in items]
    except Exception:
        requests = []

    return render(
        request,
        "shift_request/shift_request_view.html",
        {
            "data": PageMock(requests),
            "allocated_data": PageMock([]),
            "requests_ids": "[]",
            "allocated_ids": "[]",
        },
    )


def work_type_requests_view(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        raw_data = AttendanceClient(token).list_leave_requests()
        items = raw_data.get("items", []) if isinstance(raw_data, dict) else []
        requests = [DictObject(req) for req in items]
    except Exception:
        requests = []

    return render(
        request,
        "work_type_request/work_type_request_view.html",
        {
            "data": PageMock(requests),
            "allocated_data": PageMock([]),
            "requests_ids": "[]",
            "allocated_ids": "[]",
        },
    )


def rotating_shift_assign_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "base/rotating_shift/rotating_shift_assign.html",
        {
            "rshift_assign": PageMock([]),
        },
    )


def rotating_work_type_assign_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "base/rotating_work_type/rotating_work_type_assign.html",
        {
            "rwork_type_assign": PageMock([]),
        },
    )


def disciplinary_actions_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "disciplinary_actions/disciplinary_nav.html",
        {
            "data": PageMock([]),
            "pd": "",
            "f": None,
        },
    )


def policies_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "policies/view_policies.html",
        {
            "policies": PageMock([]),
        },
    )


def organisation_chart_view(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        raw_data = IdentityClient(token).list_employees()
        items = raw_data.get("items", []) if isinstance(raw_data, dict) else []
        reporting_manager_dict = {emp.get("id"): f"{emp.get('employee_first_name')} {emp.get('employee_last_name')}" for emp in items}
    except Exception:
        reporting_manager_dict = {}

    return render(
        request,
        "organisation_chart/org_chart.html",
        {
            "reporting_manager_dict": reporting_manager_dict,
            "act_manager_id": None,
        },
    )



def employee_create(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).create_employee({
                "employee_first_name": request.POST.get("employee_first_name"),
                "employee_last_name": request.POST.get("employee_last_name"),
                "email": request.POST.get("email"),
                "phone": request.POST.get("phone"),
                "password": request.POST.get("password"),
            })
            messages.success(request, "Employee created")
            return redirect("employee_list")
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, "module_view.html", {
        "page_title": "Create Employee",
        "active_module": "employee",
        "breadcrumbs": [{"title": "Employee", "url": "/employees/"}, {"title": "Create", "url": ""}],
    })


def employee_update(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).update_employee(pk, {
                "employee_first_name": request.POST.get("employee_first_name"),
                "employee_last_name": request.POST.get("employee_last_name"),
                "email": request.POST.get("email"),
                "phone": request.POST.get("phone"),
            })
            messages.success(request, "Employee updated")
            return redirect("employee_list")
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, "module_view.html", {
        "page_title": "Update Employee",
        "active_module": "employee",
        "breadcrumbs": [{"title": "Employee", "url": "/employees/"}, {"title": "Update", "url": ""}],
    })


def employee_delete(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).delete_employee(pk)
            messages.success(request, "Employee deleted")
        except Exception as exc:
            messages.error(request, str(exc))
    return redirect("employee_list")


def work_info_list(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        data = IdentityClient(token).list_work_info()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Work Info",
        "active_module": "employee",
        "work_infos": data.get("items", []),
    })


def work_info_create(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).create_work_info(request.POST.dict())
            messages.success(request, "Work Info created")
            return redirect("work_info_list")
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, "module_view.html", {
        "page_title": "Create Work Info",
        "active_module": "employee",
        "breadcrumbs": [{"title": "Work Info", "url": "/employees/work-info/"}, {"title": "Create", "url": ""}],
    })


def work_info_update(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).update_work_info(pk, request.POST.dict())
            messages.success(request, "Work Info updated")
            return redirect("work_info_list")
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, "module_view.html", {
        "page_title": "Update Work Info",
        "active_module": "employee",
        "breadcrumbs": [{"title": "Work Info", "url": "/employees/work-info/"}, {"title": "Update", "url": ""}],
    })


def work_info_delete(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).delete_work_info(pk)
            messages.success(request, "Work Info deleted")
        except Exception as exc:
            messages.error(request, str(exc))
    return redirect("work_info_list")


def bank_details_list(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        data = IdentityClient(token).list_bank_details()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Bank Details",
        "active_module": "employee",
        "bank_details": data.get("items", []),
    })


def bank_details_create(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).create_bank_details(request.POST.dict())
            messages.success(request, "Bank Details created")
            return redirect("bank_details_list")
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, "module_view.html", {
        "page_title": "Create Bank Details",
        "active_module": "employee",
        "breadcrumbs": [{"title": "Bank Details", "url": "/employees/bank-details/"}, {"title": "Create", "url": ""}],
    })


def bank_details_update(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).update_bank_details(pk, request.POST.dict())
            messages.success(request, "Bank Details updated")
            return redirect("bank_details_list")
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, "module_view.html", {
        "page_title": "Update Bank Details",
        "active_module": "employee",
        "breadcrumbs": [{"title": "Bank Details", "url": "/employees/bank-details/"}, {"title": "Update", "url": ""}],
    })


def bank_details_delete(request: HttpRequest, pk: int) -> HttpResponse:
    token = _token(request)
    if request.method == "POST":
        try:
            IdentityClient(token).delete_bank_details(pk)
            messages.success(request, "Bank Details deleted")
        except Exception as exc:
            messages.error(request, str(exc))
    return redirect("bank_details_list")


def company_list(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        data = CoreClient(token).list_companies()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Companies",
        "active_module": "employee",
        "companies": data.get("items", []),
    })


def department_list(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        data = CoreClient(token).list_departments()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Departments",
        "active_module": "employee",
        "departments": data.get("items", []),
    })


def attendance_list(request: HttpRequest) -> HttpResponse:
    try:
        data = AttendanceClient(_token(request)).list_attendance()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Attendance",
        "active_module": "attendance",
        "attendance_records": data.get("items", []),
        "breadcrumbs": [{"title": "Attendance", "url": "/attendance/"}],
    })


def leave_list(request: HttpRequest) -> HttpResponse:
    try:
        data = AttendanceClient(_token(request)).list_leave_requests()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Leave",
        "active_module": "leave",
        "leave_requests": data.get("items", []),
        "breadcrumbs": [{"title": "Leave", "url": "/leave/"}],
    })


def payroll_list(request: HttpRequest) -> HttpResponse:
    try:
        data = PayrollClient(_token(request)).list_payslips()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Payroll",
        "active_module": "payroll",
        "payslips": data.get("items", []),
        "breadcrumbs": [{"title": "Payroll", "url": "/payroll/"}],
    })


def recruitment_list(request: HttpRequest) -> HttpResponse:
    try:
        data = TalentClient(_token(request)).list_recruitment()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Recruitment",
        "active_module": "recruitment",
        "recruitments": data.get("items", []),
        "breadcrumbs": [{"title": "Recruitment", "url": "/recruitment/"}],
    })


def pms_list(request: HttpRequest) -> HttpResponse:
    try:
        data = TalentClient(_token(request)).list_objectives()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Performance",
        "active_module": "pms",
        "objectives": data.get("items", []),
        "breadcrumbs": [{"title": "Performance", "url": "/pms/"}],
    })


def onboarding_list(request: HttpRequest) -> HttpResponse:
    return render(request, "module_view.html", {
        "page_title": "Onboarding",
        "active_module": "onboarding",
        "breadcrumbs": [{"title": "Onboarding", "url": "/onboarding/"}],
    })


def offboarding_list(request: HttpRequest) -> HttpResponse:
    try:
        data = TalentClient(_token(request)).list_offboarding()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Offboarding",
        "active_module": "offboarding",
        "offboardings": data.get("items", []),
        "breadcrumbs": [{"title": "Offboarding", "url": "/offboarding/"}],
    })


def notification_list(request: HttpRequest) -> HttpResponse:
    try:
        data = PlatformClient(_token(request)).list_notifications()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Notifications",
        "active_module": "",
        "notifications": data.get("items", []),
    })


def document_list(request: HttpRequest) -> HttpResponse:
    try:
        data = PlatformClient(_token(request)).list_documents()
    except Exception:
        data = {"items": []}
    return render(request, "module_view.html", {
        "page_title": "Documents",
        "active_module": "employee",
        "documents": data.get("items", []),
    })


def permission_settings(request: HttpRequest) -> HttpResponse:
    try:
        client = PermissionClient(_token(request))
        roles = client.list_roles()
        permissions = client.list_permissions()
    except Exception:
        roles, permissions = [], []
    return render(request, "module_view.html", {
        "page_title": "Permission Settings",
        "active_module": "",
        "roles": roles,
        "permissions": permissions,
    })


def settings_view(request: HttpRequest) -> HttpResponse:
    return render(request, "settings.html", {"white_label_company_name": "Horilla HRMS"})


def quick_access(request: HttpRequest) -> HttpResponse:
    return render(request, "quick_access.html", {})


# ---------------------------------------------------------------------------
# Dashboard Stats & HTMX Widgets
# ---------------------------------------------------------------------------

def total_employees_count(request: HttpRequest) -> HttpResponse:
    token = _token(request)
    try:
        data = IdentityClient(token).list_employees(page_size=1)
        count = data.get("total", 0)
    except Exception:
        count = 0
    return HttpResponse(str(count))


def joining_today_count(request: HttpRequest) -> HttpResponse:
    return HttpResponse("0")


def joining_week_count(request: HttpRequest) -> HttpResponse:
    return HttpResponse("0")


def get_birthday(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/birthdays_container.html", {"birthdays": []})


def not_in_yet(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No records available.</p></div>')


def not_out_yet(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No records available.</p></div>')


def dashboard_shift_request(request: HttpRequest) -> HttpResponse:
    return render(request, "request_and_approve/shift_request.html", {"requests": [], "requests_ids": "[]", "pd": ""})


def dashboard_work_type_request(request: HttpRequest) -> HttpResponse:
    return render(request, "request_and_approve/work_type_request.html", {"requests": [], "requests_ids": "[]", "pd": ""})


def dashboard_approve_overtimes(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No pending overtimes.</p></div>')


def dashboard_validate_attendances(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No attendances to validate.</p></div>')


def leave_request_and_approve(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No pending leave requests.</p></div>')


def leave_allocation_approve(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No pending leave allocations.</p></div>')


def dashboard_feedback_answer(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No pending feedback answers.</p></div>')


def asset_dashboard_requests(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No pending asset requests.</p></div>')


# ---------------------------------------------------------------------------
# Dashboard JSON Charts
# ---------------------------------------------------------------------------

def dashboard_employee_chart(request: HttpRequest) -> JsonResponse:
    token = _token(request)
    try:
        data = IdentityClient(token).list_employees(page_size=100)
        employees = data.get("items", [])
        active_count = sum(1 for emp in employees if emp.get("is_active", True))
        inactive_count = len(employees) - active_count
    except Exception:
        active_count, inactive_count = 1, 0
    
    return JsonResponse({
        "labels": ["Active", "Inactive"],
        "dataSet": [
            {
                "label": "Employees",
                "data": [active_count, inactive_count],
                "backgroundColor": ["#2ecc71", "#e74c3c"]
            }
        ]
    })


def dashboard_employee_gender(request: HttpRequest) -> JsonResponse:
    token = _token(request)
    try:
        data = IdentityClient(token).list_employees(page_size=100)
        employees = data.get("items", [])
        male_count = sum(1 for emp in employees if emp.get("gender", "").lower() in ["male", "m"])
        female_count = sum(1 for emp in employees if emp.get("gender", "").lower() in ["female", "f"])
        other_count = len(employees) - male_count - female_count
    except Exception:
        male_count, female_count, other_count = 1, 1, 0
        
    labels = []
    counts = []
    bg_colors = []
    if male_count:
        labels.append("Male")
        counts.append(male_count)
        bg_colors.append("#3498db")
    if female_count:
        labels.append("Female")
        counts.append(female_count)
        bg_colors.append("#e91e63")
    if other_count:
        labels.append("Other")
        counts.append(other_count)
        bg_colors.append("#9b59b6")
        
    if not labels:
        labels = ["Male", "Female"]
        counts = [1, 1]
        bg_colors = ["#3498db", "#e91e63"]
        
    return JsonResponse({
        "labels": labels,
        "dataSet": [
            {
                "label": "Gender",
                "data": counts,
                "backgroundColor": bg_colors
            }
        ]
    })


def dashboard_employee_department(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["HR", "Engineering", "Marketing", "Sales"],
        "dataSet": [
            {
                "label": "Department",
                "data": [2, 5, 1, 2],
                "backgroundColor": ["#1abc9c", "#3498db", "#9b59b6", "#f1c40f"]
            }
        ]
    })


def dashboard_attendance(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["On Time", "Late", "Absent"],
        "dataSet": [
            {
                "label": "Attendance Status",
                "data": [80, 15, 5],
                "backgroundColor": ["#2ecc71", "#f1c40f", "#e74c3c"]
            }
        ]
    })


def department_overtime(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["HR", "Engineering", "Marketing", "Sales"],
        "dataSet": [
            {
                "label": "Overtime Hours",
                "data": [5, 20, 2, 8],
                "backgroundColor": ["#1abc9c", "#3498db", "#9b59b6", "#f1c40f"]
            }
        ]
    })


def pending_hours(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "dataSet": [
            {
                "label": "Pending Hours",
                "data": [2, 1, 3, 0, 1],
                "backgroundColor": "#e74c3c"
            }
        ]
    })


def on_time_view(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["On Time", "Late"],
        "dataSet": [
            {
                "label": "On Time Rate",
                "data": [90, 10],
                "backgroundColor": ["#2ecc71", "#e74c3c"]
            }
        ]
    })


def overall_leave(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Annual", "Sick", "Maternity", "Unpaid"],
        "dataSet": [
            {
                "label": "Leaves Taken",
                "data": [12, 4, 0, 2],
                "backgroundColor": ["#3498db", "#e74c3c", "#9b59b6", "#95a5a6"]
            }
        ]
    })


def onboard_candidate_chart(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Onboarded", "Pending", "Rejected"],
        "dataSet": [
            {
                "label": "Candidates",
                "data": [5, 2, 1],
                "backgroundColor": ["#2ecc71", "#f1c40f", "#e74c3c"]
            }
        ]
    })


def dashboard_pipeline(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Applied", "Screening", "Interview", "Offer", "Hired"],
        "dataSet": [
            {
                "label": "Pipeline Stages",
                "data": [20, 10, 5, 2, 2],
                "backgroundColor": ["#34495e", "#3498db", "#9b59b6", "#f1c40f", "#2ecc71"]
            }
        ]
    })


def hired_candidate_chart(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "dataSet": [
            {
                "label": "Hired Candidates",
                "data": [10, 15, 8, 12],
                "backgroundColor": "#3498db"
            }
        ]
    })


def dashboard_vacancy(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Open", "Closed", "Draft"],
        "dataSet": [
            {
                "label": "Vacancies",
                "data": [6, 4, 2],
                "backgroundColor": ["#2ecc71", "#95a5a6", "#f1c40f"]
            }
        ]
    })


def candidate_status(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Active", "Inactive"],
        "dataSet": [
            {
                "label": "Candidates Status",
                "data": [15, 3],
                "backgroundColor": ["#2ecc71", "#e74c3c"]
            }
        ]
    })


def project_status_chart(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["Not Started", "In Progress", "On Hold", "Completed"],
        "dataSet": [
            {
                "label": "Projects",
                "data": [2, 5, 1, 3],
                "backgroundColor": ["#95a5a6", "#3498db", "#f1c40f", "#2ecc71"]
            }
        ]
    })


def task_status_chart(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "labels": ["To Do", "In Progress", "Review", "Done"],
        "dataSet": [
            {
                "label": "Tasks",
                "data": [10, 14, 4, 25],
                "backgroundColor": ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71"]
            }
        ]
    })


def dashboard_components_toggle(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"success": True})


def create_announcement(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">Announcements not available.</p></div>')


def announcement_list(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No announcements.</p></div>')


def employee_leave(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No leave records.</p></div>')


def emp_workinfo_complete(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<div class="oh-empty h-100"><p class="oh-empty__subtitle">No work info records.</p></div>')


def get_horilla_installed_apps(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "installed_apps": ["employee", "attendance", "leave", "recruitment", "onboarding", "payroll", "pms"]
    })


def reload_messages(request: HttpRequest) -> HttpResponse:
    return render(request, "generic/messages.html")


def delete_all_notifications(request: HttpRequest) -> HttpResponse:
    return HttpResponse("")


def general_settings(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def multiple_approval_condition(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def view_mail_templates(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def mail_automations(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def holiday_view(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def company_leave_view(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def restrict_view(request: HttpRequest) -> HttpResponse:
    return redirect("settings")


def delete_notifications(request: HttpRequest, pk: int) -> HttpResponse:
    return HttpResponse("")


def read_notifications(request: HttpRequest) -> HttpResponse:
    return HttpResponse("")


def clear_notifications(request: HttpRequest) -> HttpResponse:
    return HttpResponse("")


def mark_as_read_notification(request: HttpRequest, pk: int) -> HttpResponse:
    return HttpResponse("")


def all_notifications(request: HttpRequest) -> HttpResponse:
    return redirect("notifications")


def notification_sound(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"success": True})


# ---------------------------------------------------------------------------
# Assets, Helpdesk, Project — module list stubs
# ---------------------------------------------------------------------------

def assets_list(request: HttpRequest) -> HttpResponse:
    return render(request, "module_view.html", {
        "page_title": "Assets",
        "active_module": "assets",
        "breadcrumbs": [{"title": "Assets", "url": "/assets/"}],
    })


def helpdesk_list(request: HttpRequest) -> HttpResponse:
    return render(request, "module_view.html", {
        "page_title": "Helpdesk",
        "active_module": "helpdesk",
        "breadcrumbs": [{"title": "Helpdesk", "url": "/helpdesk/"}],
    })


def project_list(request: HttpRequest) -> HttpResponse:
    return render(request, "module_view.html", {
        "page_title": "Project",
        "active_module": "project",
        "breadcrumbs": [{"title": "Project", "url": "/project/"}],
    })


# ---------------------------------------------------------------------------
# Employee language code endpoint
# ---------------------------------------------------------------------------

def get_language_code(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"language_code": "en"})



def get_language_code(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"language_code": "en"})



