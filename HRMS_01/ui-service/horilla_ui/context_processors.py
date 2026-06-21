"""Template context processors."""

import os

from django.conf import settings


def service_urls(request):
    """Inject microservice URLs and global Horilla context into every template."""
    sidebar_data = [
        {
            "app": "recruitment",
            "menu": "Recruitment",
            "img_src": "images/ui/recruitment.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/recruitment/"},
                {"menu": "Recruitment Pipeline", "redirect": "/recruitment/pipeline/"},
                {"menu": "Recruitment Survey", "redirect": "/recruitment/survey/"},
                {"menu": "Candidates", "redirect": "/recruitment/candidates/"},
                {"menu": "Interview", "redirect": "/recruitment/interview/"},
                {"menu": "Recruitment", "redirect": "/recruitment/jobs/"},
                {"menu": "Open Jobs", "redirect": "/recruitment/open-jobs/"},
                {"menu": "Stages", "redirect": "/recruitment/stages/"},
                {"menu": "Skill Zone", "redirect": "/recruitment/skill-zone/"},
            ]
        },
        {
            "app": "onboarding",
            "menu": "Onboarding",
            "img_src": "images/ui/rocket.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/onboarding/view-onboarding-dashboard"},
                {"menu": "Onboarding view", "redirect": "/onboarding/onboarding-view/"},
                {"menu": "Candidates view", "redirect": "/onboarding/candidates-view/"},
                {"menu": "Kanban view", "redirect": "/onboarding/kanban-view/"},
            ]
        },
        {
            "app": "employee",
            "menu": "Employee",
            "img_src": "images/ui/employees.svg",
            "submenu": [
                {"menu": "Profile", "redirect": "/employees/profile/"},
                {"menu": "Employees", "redirect": "/employees/"},
                {"menu": "Document Requests", "redirect": "/employees/document-requests/"},
                {"menu": "Shift Requests", "redirect": "/employees/shift-requests/"},
                {"menu": "Work Type Requests", "redirect": "/employees/work-type-requests/"},
                {"menu": "Rotating Shift Assign", "redirect": "/employees/rotating-shift-assign/"},
                {"menu": "Rotating Work Type Assign", "redirect": "/employees/rotating-work-type-assign/"},
                {"menu": "Disciplinary Actions", "redirect": "/employees/disciplinary-actions/"},
                {"menu": "Policies", "redirect": "/employees/policies/"},
                {"menu": "Organization Chart", "redirect": "/employees/org-chart/"},
            ]
        },
        {
            "app": "attendance",
            "menu": "Attendance",
            "img_src": "images/ui/attendances.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/attendance/"},
                {"menu": "Attendances", "redirect": "/attendance/attendances/"},
                {"menu": "Attendance Requests", "redirect": "/attendance/requests/"},
                {"menu": "Hour Account", "redirect": "/attendance/hour-account/"},
                {"menu": "Work Records", "redirect": "/attendance/work-records/"},
                {"menu": "Attendance Activities", "redirect": "/attendance/activities/"},
                {"menu": "Late Come Early Out", "redirect": "/attendance/late-come-early-out/"},
                {"menu": "My Attendances", "redirect": "/attendance/my-attendances/"},
            ]
        },
        {
            "app": "leave",
            "menu": "Leave",
            "img_src": "images/ui/leave.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/leave/"},
                {"menu": "My Leave Requests", "redirect": "/leave/my-requests/"},
                {"menu": "Leave Requests", "redirect": "/leave/requests/"},
                {"menu": "Leave Types", "redirect": "/leave/types/"},
                {"menu": "Assigned Leave", "redirect": "/leave/assigned/"},
                {"menu": "Leave Allocation Request", "redirect": "/leave/allocation-requests/"},
            ]
        },
        {
            "app": "payroll",
            "menu": "Payroll",
            "img_src": "images/ui/wallet-outline.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/payroll/"},
                {"menu": "Contract", "redirect": "/payroll/contracts/"},
                {"menu": "Allowances", "redirect": "/payroll/allowances/"},
                {"menu": "Deductions", "redirect": "/payroll/deductions/"},
                {"menu": "Payslips", "redirect": "/payroll/payslips/"},
                {"menu": "Loan / Advanced Salary", "redirect": "/payroll/loans/"},
                {"menu": "Encashments & Reimbursements", "redirect": "/payroll/encashments/"},
                {"menu": "Federal Tax", "redirect": "/payroll/federal-tax/"},
            ]
        },
        {
            "app": "pms",
            "menu": "Performance",
            "img_src": "images/ui/pms.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/pms/"},
                {"menu": "Objectives", "redirect": "/pms/objectives/"},
                {"menu": "360 Feedback", "redirect": "/pms/feedback/"},
                {"menu": "Meetings", "redirect": "/pms/meetings/"},
                {"menu": "Key Results", "redirect": "/pms/key-results/"},
                {"menu": "Employee Bonus Point", "redirect": "/pms/bonus-points/"},
                {"menu": "Period", "redirect": "/pms/periods/"},
                {"menu": "Question Template", "redirect": "/pms/question-templates/"},
            ]
        },
        {
            "app": "offboarding",
            "menu": "Offboarding",
            "img_src": "images/ui/exit-outline.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/offboarding/"},
                {"menu": "Exit Process", "redirect": "/offboarding/exit-process/"},
            ]
        },
        {
            "app": "assets",
            "menu": "Assets",
            "img_src": "images/ui/assets.svg",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/assets/"},
                {"menu": "Asset View", "redirect": "/assets/view/"},
                {"menu": "Asset Batches", "redirect": "/assets/batches/"},
                {"menu": "Request and Allocation", "redirect": "/assets/allocation/"},
                {"menu": "Asset History", "redirect": "/assets/history/"},
            ]
        },
        {
            "app": "helpdesk",
            "menu": "Helpdesk",
            "img_src": "images/ui/headset-solid.svg",
            "submenu": [
                {"menu": "FAQs", "redirect": "/helpdesk/faqs/"},
                {"menu": "Tickets", "redirect": "/helpdesk/tickets/"},
            ]
        },
        {
            "app": "project",
            "menu": "Project",
            "img_src": "images/ui/project.png",
            "submenu": [
                {"menu": "Dashboard", "redirect": "/project/"},
                {"menu": "Projects", "redirect": "/project/projects/"},
                {"menu": "Tasks", "redirect": "/project/tasks/"},
                {"menu": "Timesheet", "redirect": "/project/timesheets/"},
            ]
        }
    ]

    class DummyPermApp:
        def __getattr__(self, name):
            return True
        def __contains__(self, item):
            return True
        def __getitem__(self, name):
            if isinstance(name, int):
                raise IndexError
            return True

    class DummyPerms:
        def __getattr__(self, name):
            return DummyPermApp()
        def __getitem__(self, name):
            if isinstance(name, int):
                raise IndexError
            return DummyPermApp()
        def __contains__(self, item):
            return True

    return {
        # Microservice URLs
        "IDENTITY_SERVICE_URL": settings.IDENTITY_SERVICE_URL,
        "CORE_SERVICE_URL": settings.CORE_SERVICE_URL,
        "ATTENDANCE_SERVICE_URL": settings.ATTENDANCE_SERVICE_URL,
        "PAYROLL_SERVICE_URL": settings.PAYROLL_SERVICE_URL,
        "TALENT_SERVICE_URL": settings.TALENT_SERVICE_URL,
        "PLATFORM_SERVICE_URL": settings.PLATFORM_SERVICE_URL,
        "PERMISSION_SERVICE_URL": settings.PERMISSION_SERVICE_URL,

        # Global Horilla UI context (used by sidebar, navbar, login templates)
        "white_label_company_name": os.environ.get("COMPANY_NAME", "Horilla HRMS"),
        "white_label_company": None,
        "initialize_database": False,
        "current_user": request.session.get("user") or {},
        "is_authenticated": bool(request.session.get("access_token")),
        "sidebar": sidebar_data,
        "perms": DummyPerms(),
        "all_companies": [
            [
                "all",
                "All Company",
                "https://ui-avatars.com/api/?name=All+Company&background=random",
                True,
            ]
        ],
        "company_selected": True,
        "enabled_timerunner": True,
        "get_initial_notice_period": 30,
        "check_candidate_self_tracking": False,
        "check_candidate_self_tracking_rating": False,
        "get_initial_prefix": "PEP",
        "profile_edit_enabled": False,
        "LANGUAGE_CODE": "en",
    }
