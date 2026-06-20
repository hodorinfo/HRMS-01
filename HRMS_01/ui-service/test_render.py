import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla_ui.settings")
django.setup()

from django.template.loader import render_to_string
from django.test import RequestFactory
from clients.employee_views import ROUTE_TEMPLATE_MAP, DYNAMIC_ROUTE_MAP

class MockUser:
    is_authenticated = True
    def has_perm(self, perm): return True

req = RequestFactory().get("/")
req.user = MockUser()
req.session = {}

def test_templates():
    templates_to_test = set(ROUTE_TEMPLATE_MAP.values())
    for _, tpl in DYNAMIC_ROUTE_MAP:
        templates_to_test.add(tpl)
    
    success = 0
    failed = 0
    for tpl in templates_to_test:
        try:
            render_to_string(tpl, {}, request=req)
            print(f"SUCCESS: {tpl}")
            success += 1
        except Exception as e:
            print(f"FAILED: {tpl} - {type(e).__name__}: {e}")
            failed += 1
            
    print(f"\nTotal: {len(templates_to_test)}, Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    test_templates()
