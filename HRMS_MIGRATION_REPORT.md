# HRMS Migration Report — Old Horilla → New Microservices

**Report Date:** 29 June 2026  
**Scope:** Only modules that exist in the new microservices project, compared against old Horilla features  

---

## Service 1: Identity Service (Port 8001)

**Old Horilla covered:** Employee app + base (User/Auth) + accessibility + horilla_ldap + outlook_auth + horilla_documents (partial)

### Auth & Authentication

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Login | Django auth + session | ✅ Done | JWT-based login with access/refresh tokens |
| Registration | Via admin/seed | ✅ Done | Register endpoint + setup wizard |
| Password change | Django built-in | ✅ Done | `/auth/change-password` |
| Forgot/Reset password | Django built-in | ✅ Done | Email-based reset flow |
| User profile (me) | request.user | ✅ Done | `/auth/me` with update |
| Session management | Server-side sessions | ✅ Done | JWT refresh token pattern |
| **Backend %** | | **100%** | All auth features migrated |

### Employee Management

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Employee CRUD | Full (Employee model) | ✅ Done | Create, list, get, update, soft-delete |
| Employee Work Info | EmployeeWorkInformation | ✅ Done | CRUD for department/position/shift/job role |
| Employee Bank Details | EmployeeBankDetails | ✅ Done | CRUD for bank account info |
| Employee Profile | Detail + edit views | ✅ Done | React profile page with 8+ integrated tabs |
| Employee List | Table with filters | ✅ Done | EmployeeList.jsx with search/filter |
| Employee Tags | EmployeeTag | ✅ Done | CRUD via `/tags` |
| Employee Notes | EmployeeNote + NoteFiles | ⚠️ Partial | Note CRUD done; NoteFiles (attachments) pending |
| Profile Edit Features | EmployeeGeneralSetting | ✅ Done | Configurable profile edit permissions |
| Invitation email | Send invite flow | ✅ Done | `/employees/{id}/send-invitation` |
| Toggle active/inactive | is_active field | ✅ Done | `/employees/{id}/toggle-status` |
| **Backend %** | | **95%** | Note file attachments pending |

### Disciplinary Actions

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Action Types | Actiontype | ✅ Done | CRUD via `/action-types` |
| Disciplinary Actions | DisciplinaryAction | ✅ Done | CRUD via `/disciplinary-actions` |
| Document attachments | DisciplinaryActionDocument | ❌ Pending | File attachment model not migrated |
| Employee disciplinary list | In employee profile | ✅ Done | `/employees/{id}/disciplinary-actions` |
| **Backend %** | | **75%** | Core actions done, file attachments pending |

### Bonus Points & Rewards

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Bonus Points | BonusPoint | ✅ Done | CRUD via `/bonus-points` |
| Employee bonus summary | In profile | ✅ Done | `/employees/{id}/bonus-points` |
| Bonus settings | BonusPointSetting (in PMS) | ❌ Pending | Not migrated (part of PMS module) |
| **Backend %** | | **66%** | Core bonus points done, settings in PMS |

### Policies

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Company Policies | Policy + PolicyMultipleFile | ✅ Done | CRUD via `/policies` |
| Policy file attachments | PolicyMultipleFile | ❌ Pending | Multiple file upload model |
| **Backend %** | | **50%** | Policy CRUD done, file attachments pending |

### LDAP Integration

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| LDAP Settings | LDAPSettings | ✅ Done | CRUD via `/ldap` |
| LDAP sync | horilla_ldap views | ❌ Pending | Sync logic not migrated |
| **Backend %** | | **50%** | Settings CRUD done, sync logic pending |

### Outlook / Azure Auth

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Azure API config | AzureApi | ✅ Done | CRUD via `/outlook` |
| Calendar sync | OutlookEvent | ❌ Pending | Calendar event model/sync not migrated |
| **Backend %** | | **50%** | Azure config done, calendar sync pending |

### General Settings

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| General settings | EmployeeGeneralSetting | ✅ Done | CRUD via `/general-settings` |
| Profile edit features | ProfileEditFeature | ✅ Done | CRUD via `/profile-edit-features` |
| Default accessibility | DefaultAccessibility | ✅ Done | CRUD via `/accessibility` |
| **Backend %** | | **100%** | All settings models migrated |

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Login | login.html | Login.jsx | ✅ Done |
| Registration/Signup | signup.html | SignUp.jsx + CompanySetup + DepartmentSetup + JobPositionSetup | ✅ Done |
| Employee List | employee_list.html | EmployeeList.jsx | ✅ Done |
| Employee Profile | employee_view.html | MyProfile.jsx + ProfileTabs (8 tabs) | ✅ Done |
| Create Employee | employee_create.html | CreateEmployee.jsx | ✅ Done |
| Edit Employee | employee_edit.html | EditEmployee.jsx + EditProfile.jsx | ✅ Done |
| Shift Requests | shift_request.html | ❌ No route | ❌ Pending |
| Work Type Requests | work_type_request.html | ❌ No route | ❌ Pending |
| Rotating Shift Assign | rotating_shift.html | ❌ No route | ❌ Pending |
| Rotating Work Type Assign | rotating_work_type.html | ❌ No route | ❌ Pending |
| Disciplinary Actions | disciplinary.html | ❌ No route | ❌ Pending |
| Policies | policy.html | ❌ No route | ❌ Pending |
| Org Chart | org_chart.html | ❌ No route | ❌ Pending |
| Tags management | tag_list.html | ❌ No UI page | ❌ Pending |
| Notes management | notes.html | ✅ In profile tabs | ✅ Done |
| Bonus Points | bonus_point.html | ✅ In profile tabs | ✅ Done |
| LDAP settings | ldap_settings.html | ❌ No page | ❌ Pending |
| Outlook settings | outlook_settings.html | ❌ No page | ❌ Pending |
| Accessibility settings | accessibility.html | ❌ No page | ❌ Pending |
| Document Requests | document_request.html | DocumentRequests.jsx | ✅ Done |

**Frontend %:** **~50%** (9 of ~18 template groups implemented as React pages)

---

## Service 2: Core Service (Port 8002)

**Old Horilla covered:** Base app (organizational data + announcements + holidays + mail templates + approvals)

### Organizational Structure

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Companies | Company | ✅ Done | CRUD via `/companies` |
| Departments | Department | ✅ Done | CRUD via `/departments` |
| Job Positions | JobPosition | ✅ Done | CRUD via `/job-positions` |
| Job Roles | JobRole | ✅ Done | CRUD via `/job-roles` |
| Work Types | WorkType | ✅ Done | CRUD via `/work-types` |
| Employee Types | EmployeeType | ✅ Done | CRUD via `/employee-types` |
| Employee Shifts | EmployeeShift | ✅ Done | CRUD via `/shifts` |
| Shift Days | EmployeeShiftDay | ✅ Done | CRUD via `/shift-days` |
| Shift Schedules | EmployeeShiftSchedule | ✅ Done | CRUD via `/shift-schedules` |
| Rotating Work Types | RotatingWorkType | ✅ Done | CRUD via `/rotating-work-types` |
| Rotating Shift | RotatingShift | ✅ Done | CRUD via `/rotating-shifts` |
| Rotating assignments | RotatingWorkTypeAssign + RotatingShiftAssign | ✅ Done | CRUD assigned entities |
| Work Type Requests | WorkTypeRequest | ✅ Done | CRUD with approval flow |
| Shift Requests | ShiftRequest | ✅ Done | CRUD with approval flow |
| **Backend %** | | **100%** | All organization models migrated |

### Announcements

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Announcements | Announcement + AnnouncementExpire | ✅ Done | CRUD via `/announcements` |
| Comments | AnnouncementComment | ✅ Done | CRUD via `/announcement-comments` |
| Read tracking | AnnouncementView | ✅ Done | CRUD via `/announcement-views` |
| **Backend %** | | **100%** | All announcement models migrated |

### Holidays & Company Leaves

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Holidays | Holidays | ✅ Done | CRUD via `/holidays` |
| Company Leaves | CompanyLeaves | ✅ Done | CRUD via `/company-leaves` |
| **Backend %** | | **100%** | Both migrated |

### Mail Templates

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Mail Templates | HorillaMailTemplate | ✅ Done | CRUD via `/mail-templates` |
| Dynamic Email Config | DynamicEmailConfiguration | ❌ Pending | SMTP config not migrated |
| Email Log | EmailLog | ❌ Pending | Email send log not migrated |
| **Backend %** | | **33%** | Templates done, config + logs pending |

### Multiple Approvals

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Approval Conditions | MultipleApprovalCondition | ✅ Done | CRUD via `/approval-conditions` |
| Approval Managers | MultipleApprovalManagers | ✅ Done | CRUD via `/approval-managers` |
| **Backend %** | | **100%** | Both migrated |

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Company management | company.html | ❌ No dedicated page | ❌ Pending |
| Department management | department.html | ❌ No dedicated page | ❌ Pending |
| Job Position/Role | position.html | ❌ No dedicated page | ❌ Pending |
| Shift/Work Type mgmt | shift.html / work_type.html | ❌ No dedicated page | ❌ Pending |
| Holidays | holiday.html | ❌ Listed in sidebar Configuration | ❌ Pending |
| Company Leaves | company_leave.html | ❌ Listed in sidebar Configuration | ❌ Pending |
| Announcements | announcement.html | ❌ No page | ❌ Pending |
| Mail Templates | mail_template.html | ❌ Listed in sidebar Configuration | ❌ Pending |
| Multiple Approvals | approval_condition.html | ❌ Listed in sidebar Configuration | ❌ Pending |
| Reference data in forms | (select dropdowns) | ✅ Consumed in Employee forms via React Query | ✅ Done |

**Frontend %:** **~10%** (only reference data consumption done; no dedicated management pages)

---

## Service 3: Attendance Service (Port 8003)

**Old Horilla covered:** Attendance app + Leave app + Biometric + Geofencing + FaceDetection

### Attendance Core

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Attendance records | Attendance | ✅ Done | CRUD via `/attendance` |
| Clock In / Clock Out | AttendanceActivity | ✅ Done | Clock in/out endpoints + activity tracking |
| Batch Attendance | BatchAttendance | ✅ Done | Bulk attendance entry |
| Overtime tracking | AttendanceOverTime | ✅ Done | CRUD + approve endpoint |
| Late Come / Early Out | AttendanceLateComeEarlyOut | ✅ Done | CRUD via `/attendance-late-early` |
| Grace Time | GraceTime | ✅ Done | CRUD via `/grace-time` |
| Work Records | WorkRecords | ✅ Done | CRUD via `/work-records` |
| Settings | AttendanceGeneralSetting | ✅ Done | CRUD via `/attendance-settings` |
| Attendance Validation | AttendanceValidationCondition | ❌ Pending | Validation condition logic |
| Request attachments | AttendanceRequestFile | ❌ Pending | File uploads on requests |
| Request comments | AttendanceRequestComment | ❌ Pending | Comments on attendance requests |
| Offline employees | (dashboard feature) | ✅ Done | Offline count + list endpoints |
| **Backend %** | | **82%** | Core attendance fully migrated; attachments/comments/validation pending |

### Leave Management

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Leave Types | LeaveType | ✅ Done | CRUD via `/leave-types` |
| Leave Requests | LeaveRequest | ✅ Done | CRUD via `/leave-requests` |
| Available Leave (balance) | AvailableLeave | ✅ Done | CRUD via `/available-leave` |
| Leave Allocations | LeaveAllocationRequest | ✅ Done | CRUD via `/leave-allocations` |
| Restrict Leave | RestrictLeave | ✅ Done | CRUD via `/restrict-leave` |
| Compensatory Leave | CompensatoryLeaveRequest | ✅ Done | CRUD via `/compensatory-leave` (NEW - was not in old Horilla attendance) |
| Leave Approve/Reject/Cancel | Custom views | ✅ Done | PUT endpoints for approve/reject/cancel |
| Bulk Actions | Custom view | ✅ Done | POST `/request-bulk-action` |
| Leave Request attachments | LeaverequestFile | ❌ Pending | File uploads |
| Leave Request comments | LeaverequestComment | ❌ Pending | Comments |
| Leave General Settings | LeaveGeneralSetting | ❌ Pending | Settings model |
| Conditional Approvals | LeaveRequestConditionApproval | ❌ Pending | Multi-step approval |
| Employee Past Leave Restrict | EmployeePastLeaveRestrict | ❌ Pending | Restriction rules |
| **Backend %** | | **70%** | Core leave CRUD + approvals done; attachments/comments/settings pending |

### Biometrics

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Biometric Devices | BiometricDevices | ✅ Done | CRUD via `/biometric-devices` |
| Employee-Device Mapping | EmployeeBiometric / BiometricEmployees | ✅ Done | CRUD via `/biometric-employees` |
| COSEC Integration | COSECAttendanceArguments | ❌ Pending | COSEC-specific config |
| Biometric Attendance sync | BiometricAttendance (in base) | ❌ Pending | Attendance sync from devices |
| **Backend %** | | **50%** | Core device + employee mapping done; COSEC + sync pending |

### GeoFencing

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Geofence Zones | GeoFencing | ✅ Done | CRUD via `/geofencing` |
| Location-based validation | In views | ❌ Pending | Validation logic during clock in/out |
| **Backend %** | | **50%** | Zone CRUD done, validation logic pending |

### Face Detection

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Face Detection config | FaceDetection | ✅ Done | CRUD via `/face-detection` |
| Employee Face Data | EmployeeFaceDetection | ✅ Done | CRUD via `/employee-face-detection` |
| Face recognition logic | In views | ❌ Pending | Recognition algorithm/integration |
| **Backend %** | | **50%** | Config CRUD done, recognition logic pending |

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Attendance Dashboard | attendance_dashboard.html | AttendanceDashboard.jsx | ✅ Done |
| Attendance List | attendance_list.html | AttendanceList.jsx | ✅ Done |
| Attendance Requests | attendance_request.html | AttendanceRequests.jsx | ✅ Done |
| Hour Account | hour_account.html | HourAccount.jsx | ✅ Done |
| Work Records | work_records.html | WorkRecords.jsx | ✅ Done |
| Attendance Activities | attendance_activity.html | AttendanceActivities.jsx | ✅ Done |
| Late Come/Early Out | late_come_early_out.html | LateComeEarlyOut.jsx | ✅ Done |
| My Attendances | my_attendance.html | MyAttendances.jsx | ✅ Done |
| Attendance Settings | attendance_settings.html | AttendanceSettings.jsx | ✅ Done |
| Leave Dashboard | leave_dashboard.html | LeaveDashboard.jsx | ✅ Done |
| Leave Requests | leave_request.html | LeaveRequests.jsx | ✅ Done |
| My Leave Requests | my_leave_request.html | MyLeaveRequests.jsx | ✅ Done |
| Leave Types | leave_type.html | LeaveTypes.jsx | ✅ Done |
| Assigned Leave | assigned_leave.html | AssignedLeave.jsx | ✅ Done |
| Leave Allocation | leave_allocation.html | LeaveAllocation.jsx | ✅ Done |
| Leave Restrictions | restrict_leave.html | LeaveRestrictions.jsx | ✅ Done |
| Compensatory Leave | compensatory.html | CompensatoryLeave.jsx | ✅ Done |
| Biometric Devices | biometric_device.html | ❌ No page | ❌ Pending |
| GeoFencing zones | geofencing.html | ❌ No page | ❌ Pending |
| Face Detection | facedetection.html | ❌ No page | ❌ Pending |

**Frontend %:** **~85%** (17 of 20 template groups implemented)

---

## Service 4: Payroll Service (Port 8004)

**Old Horilla covered:** Payroll app (contracts, allowances, deductions, payslips, loans, reimbursements, tax)

### Contracts

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Employee Contracts | Contract | ✅ Done | CRUD via `/contracts` |
| Contract Templates | ContractTemplate | ❌ Pending | Template model not migrated |
| **Backend %** | | **50%** | Contract CRUD done, templates pending |

### Allowances & Deductions

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Allowances | Allowance | ✅ Done | CRUD via `/allowances` |
| Deductions | Deduction | ✅ Done | CRUD via `/deductions` |
| **Backend %** | | **100%** | Both migrated |

### Payslips

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Payslip CRUD | Payslip | ✅ Done | CRUD via `/payslips` |
| Payslip Download | PDF download | ✅ Done | `/payslip-download/{id}` |
| Send Payslip Email | Email payslip | ✅ Done | `/payslip-send-mail/` |
| Payslip Auto-Generate | PayslipAutoGenerate | ❌ Pending | Auto-generation config |
| Payroll calculation engine | payroll_calc.py, payslip_calc.py, tax_calc.py | ❌ Pending | Calculation logic not ported |
| **Backend %** | | **60%** | Core payslip CRUD + download/email done; auto-gen + calculation engine pending |

### Loans

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Loan Accounts | LoanAccount | ✅ Done | CRUD via `/loans` |
| **Backend %** | | **100%** | Migrated |

### Reimbursements

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Reimbursement CRUD | Reimbursement | ✅ Done | CRUD via `/reimbursements` |
| Reimbursement Approve/Reject | Custom view | ✅ Done | Approve/reject endpoint |
| Reimbursement attachments | ReimbursementMultipleAttachment | ❌ Pending | File attachments |
| Reimbursement types | ReimbursementType (tax_models) | ❌ Pending | Category model |
| Reimbursement requests | ReimbursementRequest (tax_models) | ❌ Pending | Request model |
| **Backend %** | | **40%** | Core reimbursement CRUD done; types/requests/attachments pending |

### Tax & Filing Status

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Filing Status | FilingStatus | ✅ Done | CRUD via `/filing-status` |
| Tax Brackets | TaxBracket | ❌ Pending | Tax bracket model + calculation |
| Payroll Settings | PayrollSettings | ❌ Pending | Currency, date format, etc. |
| **Backend %** | | **33%** | Filing status done, tax brackets + settings pending |

### Payroll Add-ons

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Encashment | EncashmentGeneralSettings | ❌ Pending | Leave encashment |
| Work Record | WorkRecord | ❌ Pending | Payroll work records |
| Multiple Condition | MultipleCondition | ❌ Pending | Payroll conditions |
| **Backend %** | | **0%** | None of these migrated |

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Payroll Dashboard | payroll_dashboard.html | PayrollDashboard.jsx | ✅ Done |
| Contracts | contract.html | Contract.jsx | ✅ Done |
| Allowances | allowance.html | Allowance.jsx | ✅ Done |
| Deductions | deduction.html | Deduction.jsx | ✅ Done |
| Payslips | payslip.html | Payslip.jsx | ✅ Done |
| Loan Accounts | loan_account.html | LoanAccount.jsx | ✅ Done |
| Reimbursements | reimbursement.html | Reimbursement.jsx | ✅ Done |
| Filing Status | filing_status.html | FilingStatus.jsx | ✅ Done |
| Tax Brackets | tax_bracket.html | ❌ No page | ❌ Pending |
| Encashment | encashment.html | ❌ No page | ❌ Pending |
| Payroll Settings | payroll_settings.html | ❌ No page | ❌ Pending |

**Frontend %:** **~73%** (8 of 11 template groups implemented)

---

## Service 5: Talent Service (Port 8007)

**Old Horilla covered:** Recruitment app (old) + PMS app + Onboarding app + Offboarding app

### Recruitment (PHM 2.0 - Redesigned)

Old Horilla had a traditional Recruitment pipeline. The new system has a redesigned **PHM Recruitment 2.0** with process orchestration.

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Hiring Requests | (new concept) | ✅ PHM New | Process-orchestrated hiring requests |
| Position Preparation | (new concept) | ✅ PHM New | Detailed position prep with ICP |
| Ideal Candidate Profile | (new concept) | ✅ PHM New | ICP model |
| Pipeline Stages | Stage | ✅ PHM Redesign | Replaced with PipelineStage + MasterProcess |
| Candidates | Candidate | ✅ PHM Redesign | Enhanced candidate model |
| Candidate Screening | (screening was inline) | ✅ PHM New | Dedicated screening model |
| Interview Questions | (inline) | ✅ PHM New | Dedicated question bank |
| Interview Scheduling | InterviewSchedule | ✅ Done | Migrated + enhanced |
| Interview Feedback | InterviewAnswer | ✅ PHM Redesign | Replaced with InterviewFeedback |
| Offer Details | (manual process) | ✅ PHM New | Structured offer management |
| Hiring Error Flags | (new concept) | ✅ PHM New | Error/exception tracking |
| Rejection Reasons | RejectReason | ✅ Done | Migrated |
| Job Descriptions | (inline) | ✅ PHM New | Structured JD management |
| Sourcing Channels | (new concept) | ✅ PHM New | Channel tracking |
| Process Orchestration | (none existed) | ✅ PHM New | Master templates, process steps, step dependencies, request trackers |
| **Old Recruitment Surveys** | RecruitmentSurvey | ❌ Not migrated | Replaced by process orchestration |
| **Skill Zones** | SkillZone + SkillZoneCandidate | ❌ Not migrated | Not in new system |
| **Resume parsing** | Resume model | ❌ Not migrated | Not in new system |
| **LinkedIn integration** | LinkedInAccount | ❌ Not migrated | Not in new system |

**Backend Note:** PHM is a **complete redesign** with 18 new models. Not a direct migration — ~40% feature overlap with old recruitment.

### Performance (PMS/OKR)

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Periods | Period | ✅ Done | CRUD via `/periods` |
| Objectives | Objective | ✅ Done | CRUD via `/objectives` |
| Employee Objectives | EmployeeObjective | ✅ Done | CRUD via `/employee-objectives` |
| Key Results | KeyResult | ✅ Done | CRUD via `/key-results` |
| Feedback | Feedback | ✅ Done | CRUD via `/feedback` |
| Employee Key Results | EmployeeKeyResult | ❌ Pending | Employee-specific KR tracking |
| Comments | Comment | ❌ Pending | Feedback comments |
| Key Result Feedback | KeyResultFeedback | ❌ Pending | KR-specific feedback |
| 360 Anonymous Feedback | AnonymousFeedback | ❌ Pending | Anonymous feedback model |
| Feedback Questions | QuestionTemplate + Question + QuestionOptions | ❌ Pending | Question templates |
| Meetings | Meetings | ❌ Pending | Performance meetings |
| Meeting Answers | MeetingsAnswer | ❌ Pending | Meeting Q&A |
| Bonus Point Settings | BonusPointSetting | ❌ Pending | Bonus configuration |
| Employee Bonus Points | EmployeeBonusPoint | ❌ Pending | Per-employee bonus tracking |

**Backend %:** **~29%** (5 of 17 PMS models migrated — basic OKR + Feedback only)

### Onboarding

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Onboarding Stages | OnboardingStage | ✅ Done | CRUD via `/onboarding-stages` |
| Onboarding Tasks | OnboardingTask | ✅ Done | CRUD via `/onboarding-tasks` |
| Candidate Stages | CandidateStage | ✅ Done | CRUD via `/candidate-stages` |
| Candidate Tasks | CandidateTask | ✅ Done | CRUD via `/candidate-tasks` |
| Onboarding Portal | OnboardingPortal | ✅ Done | NEW model (not in old Horilla) |
| Onboarding Candidate | OnboardingCandidate | ❌ Pending | Extended candidate tracking |
| **Backend %** | | **83%** | 5 of 6 models migrated; portal is new addition |

### Offboarding

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Offboarding processes | Offboarding | ✅ Done | CRUD via `/offboarding` |
| Offboarding Stages | OffboardingStage | ✅ Done | CRUD via `/offboarding-stages` |
| Offboarding Employees | OffboardingEmployee | ✅ Done | CRUD via `/offboarding-employees` |
| Offboarding Tasks | OffboardingTask | ✅ Done | CRUD via `/offboarding-tasks` |
| Employee Tasks | EmployeeTask | ✅ Done | CRUD via `/employee-tasks` |
| Resignation Letters | ResignationLetter | ✅ Done | CRUD via `/resignation-letters` |
| Offboarding Notes | OffboardingNote | ❌ Pending | Notes model |
| Exit Reasons | ExitReason | ❌ Pending | Exit reason tracking |
| Stage file attachments | OffboardingStageMultipleFile | ❌ Pending | File uploads on stages |
| General Settings | OffboardingGeneralSetting | ❌ Pending | Settings model |
| **Backend %** | | **60%** | 6 of 10 models migrated |

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Recruitment Dashboard | recruitment_dashboard.html | RecruitmentDashboard.jsx | ✅ Done |
| Hiring Requests | (new PHM feature) | GenericListView configured | ✅ Done |
| Candidates Hub | candidate.html | CandidatesHub.jsx | ✅ Done |
| Recruitment Settings | recruitment_settings.html | RecruitmentSettings.jsx | ✅ Done |
| Pipeline view | stage.html | ❌ No page | ❌ Pending |
| Interview scheduling | interview.html | ❌ No page | ❌ Pending |
| Offer management | (manual) | ❌ No page | ❌ Pending |
| PMS Dashboard | pms_dashboard.html | ❌ No page (empty Router) | ❌ Pending |
| Objectives | objective.html | ❌ No page | ❌ Pending |
| Key Results | key_result.html | ❌ No page | ❌ Pending |
| 360 Feedback | feedback.html | ❌ No page | ❌ Pending |
| Meetings | meeting.html | ❌ No page | ❌ Pending |
| Onboarding view | onboarding_view.html | ❌ No page (empty Router) | ❌ Pending |
| Candidates view | onboarding_candidates.html | ❌ No page | ❌ Pending |
| Offboarding Dashboard | offboarding_dashboard.html | ❌ No page (empty Router) | ❌ Pending |
| Exit Process | exit_process.html | ❌ No page | ❌ Pending |
| Resignation Letters | resignation.html | ❌ No page | ❌ Pending |

**Frontend %:** **~18%** (only 4 of ~22 template groups implemented)

---

## Service 6: Permission Service (Port 8005)

**Old Horilla covered:** Django built-in auth permissions + custom accessibility functions in sidebar

### Permissions & Roles

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| List Permissions | Django auth_permission | ✅ Done | GET `/permissions` |
| Check Permission | has_perm() | ✅ Done | POST `/permissions/check` |
| List Roles | (groups/permissions) | ✅ Done | GET `/roles` |
| Create Role | (admin interface) | ✅ Done | POST `/roles` (with permissions) |
| Assign User Roles | User.groups | ✅ Done | POST `/user-roles` |
| Role-based menu visibility | In sidebar.py | ❌ Pending | Accessibility functions not ported |
| Per-object permissions | Various checks | ❌ Pending | Fine-grained access control |

**Backend %:** **~70%** (core RBAC endpoints done; permission-based menu logic pending)

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Role Management | (Django admin) | ❌ No feature folder | ❌ Pending |
| Permission Assignment | (Django admin) | ❌ No feature folder | ❌ Pending |
| User-Role management | (Django admin) | ❌ No feature folder | ❌ Pending |

**Frontend %:** **0%** — No UI for role/permission management exists

---

## Service 7: Platform Service (Port 8006)

**Old Horilla covered:** horilla_documents + horilla_automations + notifications (django-notifications-hq) + horilla_audit

### Documents

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Document Requests | DocumentRequest | ✅ Done | CRUD via `/document-requests` |
| Documents | Document | ✅ Done | CRUD via `/documents` |
| Document Request Assignment | (not in old) | ✅ New | Assignment tracking |
| Document file upload | Multi-part upload | ⚠️ Partial | API supports attach; frontend URL-based only |
| **Backend %** | | **100%** | All document models migrated |

### Mail Automations

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Mail Automation rules | MailAutomation | ✅ Done | CRUD via `/automations` |
| Email trigger logic | (django-apscheduler) | ❌ Pending | Scheduled/triggered email execution |
| **Backend %** | | **50%** | Rules CRUD done; execution engine pending |

### Notifications

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| In-app notifications | Notification model | ✅ Done | CRUD via `/notifications` |
| Notification delivery | django-notifications-hq | ❌ Pending | Real-time delivery (WebSocket/SSE) |
| Notification preferences | (in settings) | ❌ Pending | User notification preferences |
| **Backend %** | | **33%** | CRUD done; delivery + preferences pending |

### Audit

| Feature | Old Horilla | New Status | Details |
|---------|------------|-----------|---------|
| Audit Tags | AuditTag | ✅ Done | Tagging system |
| Change history | HorillaAuditInfo + HorillaAuditLog | ❌ Pending | Change tracking models |
| **Backend %** | | **33%** | Tags done; log/history pending |

### Frontend Status

| Feature | Old Horilla Templates | New React Pages | Status |
|---------|----------------------|-----------------|--------|
| Document Requests | document_request.html | DocumentRequests.jsx | ✅ Done |
| Documents | document.html | ✅ In profile tabs | ✅ Partial |
| Notifications | notification_bell.html | ❌ No page | ❌ Pending |
| Mail Automations | mail_automation.html | ❌ Listed in sidebar Configuration | ❌ Pending |
| Audit Log | (admin) | ❌ No page | ❌ Pending |

**Frontend %:** **~30%** (document pages done, notifications/automations/audit pending)

---

## Summary Tables

### Table 1: Microservice-Level Migration Status

| Service | Backend Models | Migrated Models | Backend % | Frontend Pages | Implemented | Frontend % | Overall % | Status |
|---------|---------------|----------------|-----------|----------------|-------------|-----------|-----------|--------|
| **Identity Service** | ~30 (employee + auth + settings) | ~26 | **87%** | ~18 template groups | 9 | **50%** | **68%** | Mostly Complete |
| **Core Service** | ~23 (org data) | ~20 | **87%** | ~10 template groups | 0 (ref data only) | **10%** | **41%** | Partial |
| **Attendance Service** | ~31 (attendance + leave + bio + geo + face) | ~22 | **71%** | ~20 template groups | 17 | **85%** | **79%** | Mostly Complete |
| **Payroll Service** | ~17 (payroll + tax) | ~7 | **41%** | ~11 template groups | 8 | **73%** | **60%** | Partial |
| **Talent Service** | ~44 (recruitment + pms + onboarding + offboarding) | ~34 | **77%** | ~22 template groups | 4 | **18%** | **42%** | Partial |
| **Permission Service** | ~3 (RBAC) | ~3 | **100%** (new) | ~3 template groups | 0 | **0%** | **40%** | Started |
| **Platform Service** | ~9 (docs + notif + auto + audit) | ~7 | **78%** | ~5 template groups | 1 | **30%** | **49%** | Partial |

### Table 2: Done vs Pending Summary

| Module | Done (Old → New) | Pending (Not Yet Migrated) |
|--------|-------------------|---------------------------|
| **Auth** | Login, Register, Password mgmt, JWT tokens, Profile | — |
| **Employee** | CRUD, Work Info, Bank Details, Notes, Tags, Disciplinary, Bonus Points, Policies, Profile tabs | File attachments (NoteFiles, PolicyMultipleFile), shift/work-type request pages, rotating assign pages, org chart, disciplinary page |
| **Core Org** | All org models (Co, Dept, Pos, Role, Shift, WT, etc.), Announcements, Holidays, Company Leaves, Mail Templates, Multi-approvals | DynamicEmailConfig, EmailLog, DynamicPagination, PenaltyAccounts — all management UIs |
| **Attendance** | Core records, clock in/out, overtime, late/early, grace time, work records, settings, all leave CRUD + approvals | ValidationCondition, request attachments/comments, leave general settings, conditional approvals, past leave restrict |
| **Leave** | Leave types, requests, balance, allocations, restrictions, compensatory leave | File attachments on requests, comments, general settings, conditional approval logic |
| **Payroll** | Contracts, allowances, deductions, payslips, loans, reimbursements, filing status | Tax brackets, tax calc engine, payroll settings, encashment, auto-generate, contract templates, reimbursement types/requests |
| **Recruitment** | PHM 2.0 redesign (18 models), interview scheduling, candidates hub | Old surveys, skill zones, resume parsing, LinkedIn integration — pipeline/offer/process orchestration UIs |
| **PMS** | Objectives, key results (basic), periods, feedback | Employee KRs, comments, feedback questions, meetings, anonymous feedback, bonus point settings, question templates |
| **Onboarding** | Stages, tasks, candidate stages/tasks, portal | OnboardingCandidate tracking, full portal UI |
| **Offboarding** | Processes, stages, employees, tasks, resignation letters | Notes, exit reasons, file attachments, settings |
| **Biometrics** | Devices, employee mapping | COSEC integration, attendance sync from devices |
| **GeoFencing** | Zone CRUD | Location validation during clock in/out |
| **Face Detection** | Config CRUD, employee mapping | Recognition engine/integration |
| **Permissions** | RBAC endpoints (roles, permissions, assignment) | Menu-level access control, frontend management UI |
| **Documents** | Document requests, documents, assignments | File upload (multipart), dedicated document management page |
| **Notifications** | Notification CRUD | Delivery (WebSocket/SSE), preferences, notification UI |
| **Mail Automation** | Rule CRUD | Execution engine (scheduled/triggered) |
| **Audit** | Audit tags | Change history log, audit trail UI |
| **Accessibility** | Default settings CRUD | Frontend configuration page |
| **LDAP** | Settings CRUD | LDAP sync logic |
| **Outlook/Azure** | API settings CRUD | Calendar sync |

### Table 3: Overall Migration Totals

| Metric | Value |
|--------|-------|
| **Total Old Horilla models in scope** | ~157 (across modules being migrated) |
| **Models migrated to microservices** | ~108 (69%) |
| **Models not yet migrated** | ~49 (31%) |
| **Backend APIs implemented** | ~565 |
| **Frontend pages implemented** | 42 |
| **Frontend pages pending** | ~50+ |
| **Overall Backend Migration %** | **~69%** (108 of ~157 models in existing services) |
| **Overall Frontend Migration %** | **~45%** (42 of ~92 template groups) |
| **Overall HRMS Migration Progress** | **~55%** |

### Key Takeaways

1. **Best migrated modules**: Attendance (82% backend, 85% frontend), Leave (70% backend, 100% frontend), Employee (95% backend, 50% frontend)
2. **Most complete end-to-end**: Attendance Management — both backend and frontend are near-complete with clock in/out, approvals, overtime, etc.
3. **Backend-heavy modules (frontend lagging)**: Core Organization (87% backend, 10% frontend), Talent/PMS (77% backend, 18% frontend)
4. **Payroll needs attention**: Only 41% of old models migrated — tax engine, encashment, auto-generation, and settings are missing
5. **File attachments are a consistent gap**: Multiple old Horilla models handled file uploads (NoteFiles, PolicyMultipleFile, DisciplinaryActionDocument, LeaverequestFile, etc.) — none of these are in the new system yet
6. **Comments/threading missing**: Several old entities had comment models (LeaverequestComment, AttendanceRequestComment, ReimbursementrequestComment, etc.) — not migrated
7. **PHM Recruitment is a redesign, not a migration**: The old recruitment pipeline has been replaced with a process-orchestrated PHM 2.0 system. Feature overlap is ~40%.
8. **Configuration UIs are a blocker**: Holidays, company leaves, mail templates, multiple approvals, dynamic email config — all have backend APIs but zero frontend pages
