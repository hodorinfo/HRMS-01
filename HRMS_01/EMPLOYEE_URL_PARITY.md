# Employee URL Parity

This file tracks the old Horilla employee URLs against the new Django UI BFF and FastAPI services. Existing working routes should stay as-is; new work should add compatibility aliases first, then wire real APIs behind them.

## Current Policy

- Keep old Horilla URLs stable so imported templates do not break.
- Route UI clicks through `ui-service/clients/employee_views.py`.
- Use implemented service APIs where available.
- For missing backend APIs, return a controlled Employee shell instead of a 404/500 while the service endpoint is built.

## Implemented / Routed

| Old Horilla URL | BFF handling | Backend/service status | Notes |
| --- | --- | --- | --- |
| `/employee/` | `employee_list` | Identity employees | Employee card/list page. |
| `/employee/employee-view/` | `employee_list` | Identity employees | Old employee index alias. |
| `/employee/employee-view/<id>/` | `employee_detail` | Identity + profile helper APIs | Employee detail/profile view. |
| `/employee/employee-profile/` | `employee_profile_view` | Identity current employee | Own profile view. |
| `/employee/edit-profile/` | `edit_profile_view` | Identity/work/bank APIs | Own/selected profile edit. |
| `/employee/employee-view-new/` | `employee_create` | Identity + work/bank APIs | Create employee form. |
| `/employee/employee-view-update/<id>/` | `employee_update` | Identity + work/bank APIs | Edit employee form. |
| `/employee/employee-archive/<id>/` | `employee_archive_toggle` | Identity soft archive | Archive/unarchive action. |
| `/employee/employee-delete/<id>/` | `employee_delete` | Identity delete/archive | Old delete action maps to archive. |
| `/employee/about-tab[/<id>]` | `employee_about_tab` | Identity/work/bank/payroll | Supports no-id current employee fallback. |
| `/employee/shift-tab[/<id>]` | `employee_shift_tab` | Core shift/work type requests | Supports no-id current employee fallback. Rotating assignment API pending. |
| `/employee/profile-attendance-tab/` | `profile_attendance_tab` | Attendance API | Own/current profile attendance tab. |
| `/employee/attendance-tab/` | `profile_attendance_tab` | Attendance API | Detail alias. |
| `/employee/leave-tab[/<id>]` | `leave_profile_tab` | Attendance leave API | Supports no-id fallback. |
| `/employee/document-tab[/<id>]` | `profile_documents_tab` | Platform documents | Supports upload/create/update/delete actions. |
| `/employee/document-request-view/` | `document_requests_view` | Platform document requests/documents | Main document request page. |
| `/employee/document-request-create/` | create form/save | Platform document requests | Modal-compatible create. |
| `/employee/document-create/<employee_id>` | `document_create` | Platform documents | Profile document create. |
| `/employee/file-upload/<document_id>` | `file_upload` | Platform documents | Upload/update file path. |
| `/employee/update-document-title/<document_id>` | `update_document_title` | Platform documents | Inline title update. |
| `/employee/document-approve/<id>` | `document_approve` | Platform documents | Approve status. |
| `/employee/document-reject/<id>` | `document_reject` | Platform documents | Reject status. |
| `/employee/document-delete/<id>` | `document_delete` | Platform documents | Delete document. |
| `/employee/shift-request-view/` | `shift_requests_view` | Core shift requests | Old list alias. |
| `/employee/work-type-request-view/` | `work_type_requests_view` | Core work type requests | Old list alias. |
| `/employee/shift-request-create` | `shift_request_create` | Core shift requests | Profile tab form POST. |
| `/employee/work-type-request-create` | `work_type_request_create` | Core work type requests | Profile tab form POST. |
| `/employee/rotating-shift-assign[-view]/` | `rotating_shift_assign_view` | Shell | Core rotating assignment API still pending. |
| `/employee/rotating-work-type-assign[-view]/` | `rotating_work_type_assign_view` | Shell | Core rotating assignment API still pending. |
| `/employee/disciplinary-actions/` | `disciplinary_actions_view` | Shell | Service model/API pending. |
| `/employee/policies/`, `/employee/search-policies/` | `policies_view` | Shell | Service model/API pending. |
| `/employee/org-chart/`, `/employee/organisation-chart/` | `organisation_chart_view` | Identity employees | Basic org chart context. |

## Profile Tab Aliases

These old profile tab URLs are now accepted with or without an employee id. Without an id, the BFF resolves the current logged-in employee when possible.

- `/employee/payroll-tab/`
- `/employee/allowances-deductions-tab/`
- `/employee/view-penalties`
- `/employee/profile-asset-tab/`
- `/employee/performance-tab/`
- `/employee/employee-history-tab/`
- `/employee/employee-groups-tab/`
- `/employee/employee-note-tab/`
- `/employee/employee-mail-log-tab/`
- `/employee/bonus-points-tab/`
- `/employee/employee-interview-tab/`
- `/employee/search-resignation-request/`

## Pending API Groups

These URLs are intentionally mapped to a safe placeholder shell for now, so imported templates do not crash while the matching service API is built.

- Rotating shift assignment CRUD/import/export/select/filter endpoints.
- Rotating work type assignment CRUD/import/export/select/filter endpoints.
- Disciplinary action type and action CRUD endpoints.
- Policy CRUD, attachment upload/remove, policy detail endpoints.
- Employee bulk mail/bulk update/import/export endpoints.
- Dynamic create endpoints for department/job position/job role/work type/shift/employee type.
- Profile image upload/remove endpoints.
- Permission/account/mail-log/password utility endpoints.

## Next Backend Work

1. Add Core service APIs for rotating shift assignments and rotating work type assignments.
2. Add Employee/Platform service APIs for policies and disciplinary actions.
3. Add BFF forms/actions for bulk employee operations and import/export.
4. Replace placeholder shells with real old-Horilla-like templates as each API lands.
