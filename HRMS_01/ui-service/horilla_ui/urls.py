"""URL configuration for Horilla UI BFF."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from clients import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("recruitment/", include("horilla_ui.recruitment_urls")),
    path("employee/", include("horilla_ui.employee_urls")),
    path("onboarding/", include("horilla_ui.onboarding_urls")),

    # Auth
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("reset-password/", views.reset_password_view, name="reset-password"),
    path("signup/", views.signup_view, name="signup"),

    # Core HR modules
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<int:pk>/", views.employee_detail, name="employee_detail"),
    path("employees/create/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/update/", views.employee_update, name="employee_update"),
    path("employees/<int:pk>/delete/", views.employee_delete, name="employee_delete"),
    path("employees/work-info/", views.work_info_list, name="work_info_list"),
    path("employees/work-info/create/", views.work_info_create, name="work_info_create"),
    path("employees/work-info/<int:pk>/update/", views.work_info_update, name="work_info_update"),
    path("employees/work-info/<int:pk>/delete/", views.work_info_delete, name="work_info_delete"),
    path("employees/bank-details/", views.bank_details_list, name="bank_details_list"),
    path("employees/bank-details/create/", views.bank_details_create, name="bank_details_create"),
    path("employees/bank-details/<int:pk>/update/", views.bank_details_update, name="bank_details_update"),
    path("employees/bank-details/<int:pk>/delete/", views.bank_details_delete, name="bank_details_delete"),
    path("companies/", views.company_list, name="company_list"),
    path("departments/", views.department_list, name="department_list"),
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("leave/", views.leave_list, name="leave_list"),
    path("payroll/", views.payroll_list, name="payroll_list"),
    path("recruitment/", views.recruitment_list, name="recruitment_list"),
    path("pms/", views.pms_list, name="pms_list"),
    path("onboarding/", views.onboarding_list, name="onboarding_list"),
    path("offboarding/", views.offboarding_list, name="offboarding_list"),
    path("notifications/", views.notification_list, name="notifications"),
    path("notifications/list/", views.notification_list, name="notification_list"),
    path("documents/", views.document_list, name="document_list"),
    path("settings/permissions/", views.permission_settings, name="permission_settings"),

    # Misc stubs referenced by templates
    path("settings/", views.settings_view, name="settings"),
    path("quick-access/", views.quick_access, name="quick_access"),

    # Dashboard HTMX/Stats
    path("total-employees-count/", views.total_employees_count, name="total-employees-count"),
    path("joining-today-count/", views.joining_today_count, name="joining-today-count"),
    path("joining-week-count/", views.joining_week_count, name="joining-week-count"),
    path("get-birthday/", views.get_birthday, name="get-birthday"),
    path("not-in-yet/", views.not_in_yet, name="not-in-yet"),
    path("not-out-yet/", views.not_out_yet, name="not-out-yet"),
    path("dashboard-shift-request/", views.dashboard_shift_request, name="dashboard-shift-request"),
    path("dashboard-work-type-request/", views.dashboard_work_type_request, name="dashboard-work-type-request"),
    path("dashboard-approve-overtimes/", views.dashboard_approve_overtimes, name="dashboard-approve-overtimes"),
    path("dashboard-validate-attendances/", views.dashboard_validate_attendances, name="dashboard-validate-attendances"),
    path("leave-request-and-approve/", views.leave_request_and_approve, name="leave-request-and-approve"),
    path("leave-allocation-approve/", views.leave_allocation_approve, name="leave-allocation-approve"),
    path("dashboard-feedback-answer/", views.dashboard_feedback_answer, name="dashboard-feedback-answer"),
    path("asset-dashboard-requests/", views.asset_dashboard_requests, name="asset-dashboard-requests"),
    path("dashboard-components-toggle/", views.dashboard_components_toggle, name="dashboard-components-toggle"),
    path("create-announcement/", views.create_announcement, name="create-announcement"),
    path("announcement-list/", views.announcement_list, name="announcement-list"),
    path("employee-leave/", views.employee_leave, name="employee-leave"),
    path("emp-workinfo-complete/", views.emp_workinfo_complete, name="emp-workinfo-complete"),

    # Redirect/Compatibility aliases
    path("home-page/", views.dashboard, name="home-page"),
    path("candidate-view/", views.recruitment_list, name="candidate-view"),
    path("employee-view/", views.employee_list, name="employee-view"),

    # Dashboard Charts JSON
    path("employee/dashboard-employee/", views.dashboard_employee_chart, name="dashboard-employee-chart"),
    path("employee/dashboard-employee-gender/", views.dashboard_employee_gender, name="dashboard-employee-gender"),
    path("employee/dashboard-employee-department/", views.dashboard_employee_department, name="dashboard-employee-department"),
    path("attendance/dashboard-attendance/", views.dashboard_attendance, name="dashboard-attendance"),
    path("attendance/department-overtime-chart/", views.department_overtime, name="department-overtime"),
    path("attendance/pending-hours/", views.pending_hours, name="pending-hours"),
    path("attendance/on-time-view/", views.on_time_view, name="on-time-view"),
    path("leave/overall-leave/", views.overall_leave, name="overall-leave"),
    path("onboarding/onboard-candidate-chart/", views.onboard_candidate_chart, name="onboard-candidate-chart"),
    path("recruitment/dashboard-pipeline/", views.dashboard_pipeline, name="dashboard-pipeline"),
    path("recruitment/hired-candidate-chart/", views.hired_candidate_chart, name="hired-candidate-chart"),
    path("recruitment/dashboard-vacancy/", views.dashboard_vacancy, name="dashboard-vacancy"),
    path("recruitment/candidate-status/", views.candidate_status, name="candidate-status"),
    path("project/project-status-chart/", views.project_status_chart, name="project-status-chart"),
    path("project/task-status-chart/", views.task_status_chart, name="task-status-chart"),
    path("get-horilla-installed-apps/", views.get_horilla_installed_apps, name="get-horilla-installed-apps"),
    path("reload-messages/", views.reload_messages, name="reload-messages"),
    path("delete-all-notifications/", views.delete_all_notifications, name="delete-all-notifications"),
    path("settings/general/", views.general_settings, name="general-settings"),
    path("settings/multiple-approvals/", views.multiple_approval_condition, name="multiple-approval-condition"),
    path("settings/mail-templates/", views.view_mail_templates, name="view-mail-templates"),
    path("settings/mail-automations/", views.mail_automations, name="mail-automations"),
    path("settings/holidays/", views.holiday_view, name="holiday-view"),
    path("settings/company-leaves/", views.company_leave_view, name="company-leave-view"),
    path("settings/restrict-leaves/", views.restrict_view, name="restrict-view"),
    path("notifications/delete/<int:pk>/", views.delete_notifications, name="delete-notifications"),
    path("notifications/read/", views.read_notifications, name="read-notifications"),
    path("notifications/clear/", views.clear_notifications, name="clear-notifications"),
    path("notifications/mark-read/<int:pk>/", views.mark_as_read_notification, name="mark-as-read-notification"),
    path("notifications/all/", views.all_notifications, name="all-notifications"),
    path("notifications/sound/", views.notification_sound, name="notification-sound"),

    # ── Recruitment ──────────────────────────────────────────────────────────
    path("recruitment/pipeline/", views.recruitment_list, name="recruitment-pipeline"),
    path("recruitment/survey/", views.recruitment_list, name="recruitment-survey"),
    path("recruitment/candidates/", views.recruitment_list, name="recruitment-candidates"),
    path("recruitment/interview/", views.recruitment_list, name="recruitment-interview"),
    path("recruitment/jobs/", views.recruitment_list, name="recruitment-jobs"),
    path("recruitment/open-jobs/", views.recruitment_list, name="recruitment-open-jobs"),
    path("recruitment/stages/", views.recruitment_list, name="recruitment-stages"),
    path("recruitment/skill-zone/", views.recruitment_list, name="recruitment-skill-zone"),

    # ── Employee ─────────────────────────────────────────────────────────────
    path("employees/profile/", views.employee_profile_view, name="employee-profile"),
    path("employees/document-requests/", views.document_requests_view, name="employee-document-requests"),
    path("employees/shift-requests/", views.shift_requests_view, name="employee-shift-requests"),
    path("employees/work-type-requests/", views.work_type_requests_view, name="employee-work-type-requests"),
    path("employees/rotating-shift-assign/", views.rotating_shift_assign_view, name="employee-rotating-shift-assign"),
    path("employees/rotating-work-type-assign/", views.rotating_work_type_assign_view, name="employee-rotating-work-type-assign"),
    path("employees/disciplinary-actions/", views.disciplinary_actions_view, name="employee-disciplinary-actions"),
    path("employees/policies/", views.policies_view, name="employee-policies"),
    path("employees/org-chart/", views.organisation_chart_view, name="employee-org-chart"),

    # ── Attendance ────────────────────────────────────────────────────────────
    path("attendance/attendances/", views.attendance_list, name="attendance-attendances"),
    path("attendance/requests/", views.attendance_list, name="attendance-requests"),
    path("attendance/hour-account/", views.attendance_list, name="attendance-hour-account"),
    path("attendance/work-records/", views.attendance_list, name="attendance-work-records"),
    path("attendance/activities/", views.attendance_list, name="attendance-activities"),
    path("attendance/late-come-early-out/", views.attendance_list, name="attendance-late-come-early-out"),
    path("attendance/my-attendances/", views.attendance_list, name="attendance-my-attendances"),

    # ── Leave ─────────────────────────────────────────────────────────────────
    path("leave/my-requests/", views.leave_list, name="leave-my-requests"),
    path("leave/requests/", views.leave_list, name="leave-requests"),
    path("leave/types/", views.leave_list, name="leave-types"),
    path("leave/assigned/", views.leave_list, name="leave-assigned"),
    path("leave/allocation-requests/", views.leave_list, name="leave-allocation-requests"),

    # ── Payroll ───────────────────────────────────────────────────────────────
    path("payroll/contracts/", views.payroll_list, name="payroll-contracts"),
    path("payroll/allowances/", views.payroll_list, name="payroll-allowances"),
    path("payroll/deductions/", views.payroll_list, name="payroll-deductions"),
    path("payroll/payslips/", views.payroll_list, name="payroll-payslips"),
    path("payroll/loans/", views.payroll_list, name="payroll-loans"),
    path("payroll/encashments/", views.payroll_list, name="payroll-encashments"),
    path("payroll/federal-tax/", views.payroll_list, name="payroll-federal-tax"),

    # ── Performance (PMS) ─────────────────────────────────────────────────────
    path("pms/objectives/", views.pms_list, name="pms-objectives"),
    path("pms/feedback/", views.pms_list, name="pms-feedback"),
    path("pms/meetings/", views.pms_list, name="pms-meetings"),
    path("pms/key-results/", views.pms_list, name="pms-key-results"),
    path("pms/bonus-points/", views.pms_list, name="pms-bonus-points"),
    path("pms/periods/", views.pms_list, name="pms-periods"),
    path("pms/question-templates/", views.pms_list, name="pms-question-templates"),

    # ── Offboarding ───────────────────────────────────────────────────────────
    path("offboarding/exit-process/", views.offboarding_list, name="offboarding-exit-process"),

    # ── Assets ────────────────────────────────────────────────────────────────
    path("assets/", views.assets_list, name="assets_list"),
    path("assets/view/", views.assets_list, name="assets-view"),
    path("assets/batches/", views.assets_list, name="assets-batches"),
    path("assets/allocation/", views.assets_list, name="assets-allocation"),
    path("assets/history/", views.assets_list, name="assets-history"),

    # ── Helpdesk ──────────────────────────────────────────────────────────────
    path("helpdesk/", views.helpdesk_list, name="helpdesk_list"),
    path("helpdesk/faqs/", views.helpdesk_list, name="helpdesk-faqs"),
    path("helpdesk/tickets/", views.helpdesk_list, name="helpdesk-tickets"),

    # ── Project ───────────────────────────────────────────────────────────────
    path("project/", views.project_list, name="project_list"),
    path("project/projects/", views.project_list, name="project-projects"),
    path("project/tasks/", views.project_list, name="project-tasks"),
    path("project/timesheets/", views.project_list, name="project-timesheets"),

    # ── Employee misc ─────────────────────────────────────────────────────────
    path("employee/get-language-code/", views.get_language_code, name="get-language-code"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
