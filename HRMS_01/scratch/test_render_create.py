import os
import sys
import django

# Set up django environment
sys.path.append("/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla_ui.settings")
django.setup()

from django.test import RequestFactory
from clients.views import employee_create

rf = RequestFactory()
request = rf.get("/employees/create/")
# Mock session and user
request.session = {}
request.user = type('User', (), {'is_authenticated': True, 'employee_get': None})()

try:
    response = employee_create(request)
    print("STATUS CODE:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
