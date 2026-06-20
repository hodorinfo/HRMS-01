"""
employee_views.py

Generic BFF view handler for all Employee module routes.
Maps each URL path to the correct template in templates/employee/.
"""
from django.shortcuts import render, redirect

def _is_authenticated(request):
    """Use the same auth check as the rest of the BFF views."""
    return bool(request.session.get("access_token"))

# Full route → template map (path after /employee/)
ROUTE_TEMPLATE_MAP = {
    "":                              "employee/templates/employee_personal_info/employee_list.html",
    "employees":                     "employee/templates/employee_personal_info/employee_list.html",
    "employees/":                    "employee/templates/employee_personal_info/employee_list.html",
    "employee-view":                 "employee/templates/employee_personal_info/employee_view.html",
    "employee-card":                 "employee/templates/employee_personal_info/employee_card.html",
    "employee-list":                 "employee/templates/employee_personal_info/employee_list.html",
    "employee-create":               "employee/templates/employee_personal_info/employee_create_form.html",
    "employee-view-new":             "employee/templates/employee/create_form/form_view.html",
    
    # Submenus
    "profile":                       "employee/templates/employee_personal_info/employee_view.html",
    "document-requests":             "employee/templates/documents/document_requests.html",
    "shift-requests":                "shift_request/shift_request_view.html",
    "work-type-requests":            "work_type_request/work_type_request_view.html",
    "rotating-shift-assign":         "employee/templates/base/rotating_shift/rotating_shift_assign.html",
    "rotating-work-type-assign":     "employee/templates/base/rotating_work_type/rotating_work_type_assign.html",
    "org-chart":                     "employee/templates/organisation_chart/org_chart.html",
    "company-policies":              "employee/templates/policies/records.html",
    "company-policies/":             "employee/templates/policies/records.html",
    "policies":                      "employee/templates/policies/records.html",
    "disciplinary-actions":          "employee/templates/disciplinary_actions/disciplinary_records.html",
    "disciplinary-actions/":         "employee/templates/disciplinary_actions/disciplinary_records.html",

    # Dashboard
    "dashboard":                     "employee/templates/employee/dashboard/dashboard_employee.html",

    # Settings
    "settings":                      "employee/templates/settings/settings.html",
}

DYNAMIC_ROUTE_MAP = [
    ("employee-view/",               "employee/templates/employee/view/individual.html"),
    ("employee-update/",             "employee/templates/employee_personal_info/employee_update_form.html"),
]

def generic_employee_view(request, route=""):
    """Route all /employee/<route>/ paths to their templates."""
    if not _is_authenticated(request):
        return redirect("login")
    
    # Normalize trailing slash
    route = route.strip("/")

    # 1. Exact match
    if route in ROUTE_TEMPLATE_MAP:
        template = ROUTE_TEMPLATE_MAP[route]
        return render(request, template, _ctx(route))

    # 2. Prefix/dynamic match
    for prefix, template in DYNAMIC_ROUTE_MAP:
        if route.startswith(prefix.rstrip("/")):
            return render(request, template, _ctx(route))

    # 3. Fallback to generic module view
    return render(request, "module_view.html", {
        "page_title": "Employee — " + route.replace("-", " ").title(),
        "active_module": "employee",
        "breadcrumbs": [
            {"title": "Employee", "url": "/employee/"},
            {"title": route.replace("-", " ").title(), "url": ""},
        ],
    })

def _ctx(route):
    """Build a minimal template context."""
    return {
        "page_title": route.replace("-", " ").title() if route else "Employee",
        "active_module": "employee",
    }
