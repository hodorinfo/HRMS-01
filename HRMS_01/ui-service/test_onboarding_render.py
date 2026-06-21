import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError, TemplateDoesNotExist

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla_ui.settings')
django.setup()

from clients.onboarding_views import ROUTE_TEMPLATE_MAP, DYNAMIC_ROUTE_MAP
from clients.recruitment_views import ROUTE_TEMPLATE_MAP as REC_MAP, DYNAMIC_ROUTE_MAP as REC_DYN_MAP
# Mock request
class MockRequest:
    def __init__(self):
        self.META = {}
        self.GET = {}
        self.POST = {}
        self.user = type('MockUser', (), {'is_authenticated': True, 'is_superuser': True})()
        
    def build_absolute_uri(self):
        return "http://localhost:8008/"

def test_templates():
    templates_to_test = set()
    
    # Gather from ROUTE_TEMPLATE_MAP
    for route, template in ROUTE_TEMPLATE_MAP.items():
        templates_to_test.add((route, template))
        
    # Gather from DYNAMIC_ROUTE_MAP
    for prefix, template in DYNAMIC_ROUTE_MAP:
        templates_to_test.add((prefix, template))

    print(f"Attempting to dry-run render {len(templates_to_test)} onboarding templates...\n")
    
    success_count = 0
    failed_templates = []
    
    for route, template in templates_to_test:
        try:
            render_to_string(template, {'request': MockRequest()})
            success_count += 1
        except Exception as e:
            failed_templates.append((template, str(e)))

    print("\n--- RENDER TEST RESULTS ---")
    print(f"Success: {success_count}/{len(templates_to_test)} ({success_count/len(templates_to_test)*100:.1f}%)")
    
    if failed_templates:
        print(f"Failed: {len(failed_templates)}")
        for template, error in failed_templates:
            print(f"  [x] {template}: {error}")
        exit(1)
    else:
        print("All onboarding templates successfully rendered!")
        exit(0)

if __name__ == "__main__":
    test_templates()
