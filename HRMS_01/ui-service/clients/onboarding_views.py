import re
from django.shortcuts import render
from django.template import TemplateDoesNotExist

ROUTE_TEMPLATE_MAP = {
    # Candidates
    "candidate-creation": "onboarding/candidate_creation_form.html",
    "candidates-view": "onboarding/candidates_view.html",
    "candidates-view/": "onboarding/candidates_view.html",
    "hired-candidates-view": "onboarding/candidates_view.html",
    "candidate-filter": "onboarding/candidate_filter.html",
    "candidate-tasks-status": "onboarding/candidate_task.html",
    "onboarding-candidate-bulk-delete/": "onboarding/candidates_view.html",

    # Pipeline & Dashboard
    "view-onboarding-dashboard": "onboarding/dashboard.html",
    "onboarding-view": "onboarding/onboarding_view.html",
    "onboarding-view/": "onboarding/onboarding_view.html",
    "kanban-view": "onboarding/kanban/kanban.html",

    # Settings & Tasks
    "task-creation": "onboarding/task_form.html",
    "change-task-status": "onboarding/task_view.html",
    "update-joining": "onboarding/onboarding_view.html",
    "candidate-sequence-update": "onboarding/onboarding_view.html",
    "stage-sequence-update": "onboarding/onboarding_view.html",
    "update-probation-end": "onboarding/onboarding_view.html",
    "task-report-onboarding": "onboarding/onboarding_view.html",
    "update-offer-letter-status": "onboarding/onboarding_view.html",
    "add-to-rejected-candidates": "onboarding/onboarding_view.html",
    "candidate-select-filter-onboarding": "onboarding/onboarding_view.html",
    "candidate-select/": "onboarding/onboarding_view.html",
    "offer-letter-bulk-status-update/": "onboarding/onboarding_view.html",
    "email-send": "onboarding/onboarding_view.html",
}

DYNAMIC_ROUTE_MAP = [
    # Stages
    ("stage-creation/", "onboarding/stage_form.html"),
    ("stage-update/", "onboarding/stage_update.html"),
    ("stage-delete/", "onboarding/onboarding_view.html"),
    ("stage-name-update/", "onboarding/stage_update.html"),

    # Tasks
    ("task-delete/", "onboarding/onboarding_view.html"),
    ("task-update/", "onboarding/task_update.html"),
    ("assign-task/", "onboarding/task_form.html"),
    ("get-status/", "onboarding/task_view.html"),

    # Candidates
    ("candidate-update/", "onboarding/candidate_update.html"),
    ("candidate-delete/", "onboarding/candidates_view.html"),
    ("candidate-single-view/", "onboarding/single_view.html"),
    ("candidate-task-update/", "onboarding/task_update.html"),
    ("candidate-stage-update/", "onboarding/stage_update.html"),
    ("delete-candidate-rejection/", "onboarding/candidates_view.html"),
    ("send-mail/", "onboarding/send_mail_form.html"),

    # Employee Conversion / User Forms
    ("user-creation/", "onboarding/user_creation.html"),
    ("profile-view/", "onboarding/profile_view.html"),
    ("employee-creation/", "onboarding/employee_creation.html"),
    ("employee-bank-details/", "onboarding/employee_bank_details.html"),
    ("welcome-aboard", "onboarding/welcome_aboard.html"),
    ("welcome-aboard/", "onboarding/welcome_aboard.html"),
]

from .api_clients import TalentClient

def generic_onboarding_view(request, route=""):
    """
    Catch-all view for the Onboarding module frontend endpoints.
    """
    clean_route = route.strip()
    
    context = {"request": request}
    # We will use TalentClient to fetch live data if authenticated
    if bool(request.session.get("access_token")):
        client = TalentClient(token=request.session.get("access_token"))
        
        # Phase 1 Integration: Intercept Dashboard and Kanban to inject live data
        if clean_route in ("view-onboarding-dashboard", "onboarding-view", "onboarding-view/"):
            try:
                data = client.get_onboarding_dashboard()
                context.update(data)
            except Exception as e:
                print(f"Failed to fetch onboarding dashboard: {e}")
                context["api_error"] = str(e)
                
        elif clean_route == "kanban-view":
            try:
                data = client.get_onboarding_kanban()
                context.update(data)
            except Exception as e:
                print(f"Failed to fetch onboarding kanban: {e}")
                context["api_error"] = str(e)

    # 1. Exact match check
    if clean_route in ROUTE_TEMPLATE_MAP:
        template_name = ROUTE_TEMPLATE_MAP[clean_route]
        print(f"Matched STATIC route '{clean_route}' -> {template_name}")
        try:
            return render(request, template_name, context)
        except TemplateDoesNotExist:
            print(f"ERROR: Template {template_name} not found!")

    # 2. Dynamic route match check
    for prefix, template_name in DYNAMIC_ROUTE_MAP:
        if clean_route.startswith(prefix):
            print(f"Matched DYNAMIC route '{clean_route}' (prefix {prefix}) -> {template_name}")
            try:
                return render(request, template_name, context)
            except TemplateDoesNotExist:
                print(f"ERROR: Template {template_name} not found!")
                break

    # Fallback to a default view
    print(f"Unmatched route '{clean_route}', falling back to default module view.")
    context.update({
        "module_name": "Onboarding",
        "route_attempted": route,
    })
    return render(request, "module_view.html", context)
