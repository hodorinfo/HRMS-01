# Phase 4 - Employee Profile UI Parity Slice

## Goal

Old Horilla ke Employee dropdown ke first option, `Profile`, ko HRMS_02 project mein old Horilla ke visual shell ke close lana.

## Changes

- Added `ui-service/templates/employee/profile/profile_parity.html`
  - Old Horilla `index.html` shell extend karta hai.
  - Profile header, avatar, edit action, previous/next navigation, contact fields, and tab row old Horilla classes/assets ke saath render hote hain.

- Updated `ui-service/clients/views.py`
  - `employee_detail` and `employee_profile_view` ab old-style profile parity template render karte hain.
  - `employee_about_html` added for Personal Information + Work Information cards.
  - Added profile tab fragments:
    - Attendance
    - Leave
    - Documents
    - Payroll placeholder
    - Allowance & Deduction placeholder
    - Penalty Account placeholder
    - Assets placeholder
    - Performance placeholder
    - Bonus Points placeholder
    - Scheduled Interview placeholder
    - Resignation placeholder

- Updated `ui-service/clients/employee_views.py`
  - `/employee/employee-profile/`
  - `/employee/about-tab/<id>`
  - `/employee/shift-tab/<id>`
  now delegate to real BFF views instead of generic placeholder templates.

- Updated `ui-service/horilla_ui/urls.py`
  - Root-level compatibility endpoints added for profile tabs.

## Follow-up Correction

- Restored old Horilla `Bank Information` section inside the About tab.
- Added `Contract details` tab content with old Horilla style sticky table:
  - Contract
  - Start Date
  - End Date
  - Wage Type
  - Basic Salary
  - Actions
- Added old Horilla style 3-dot column selector:
  - Select All Columns
  - Unselect All Columns
  - checkbox controls for profile tabs
- Bank data now reads from identity-service bank details when available.
- Contract data now reads from payroll-service contracts when available, with a fallback row from employee work info.

## Why

HRMS_02 mein `/employee/...` routes catch-all generic handler se ja rahe the, isliye profile page old Horilla jaisa render nahi ho raha tha. Is slice mein catch-all ko profile-specific routes ke liye real view pe delegate kiya gaya.

## Verification

Run:

```bash
cd /home/hodorinfo1/Downloads/HRMS_02/HRMS_01
PYTHONPYCACHEPREFIX=/tmp/hrms02_ui_pycache python3 -m compileall ui-service -q
```

Then Docker run karke browser open:

```text
http://localhost:8000/employee/employee-profile/
```

## Remaining

- Deeper actions ko service-backed banana:
  - edit profile parity
  - attendance actions
  - leave actions
  - document upload/download
  - contract edit/delete actions
  - payroll/assets/performance real service data
