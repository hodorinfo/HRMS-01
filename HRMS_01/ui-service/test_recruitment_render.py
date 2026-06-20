import os
import django
from django.template.loader import render_to_string

# Set up Django environment manually
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla_ui.settings')
django.setup()

from clients.recruitment_views import ROUTE_TEMPLATE_MAP, DYNAMIC_ROUTE_MAP

def test_all_recruitment_templates():
    failed = []
    success_count = 0
    total = 0

    templates_to_test = set(ROUTE_TEMPLATE_MAP.values())
    for _, tmpl in DYNAMIC_ROUTE_MAP:
        templates_to_test.add(tmpl)

    print(f"Attempting to dry-run render {len(templates_to_test)} recruitment templates...")
    
    for template in templates_to_test:
        total += 1
        try:
            # We provide some mock contexts commonly expected by templates
            context = {
                "request": type("MockRequest", (), {"session": {}, "user": None, "GET": {}})(),
                "messages": [],
                "page_title": "Recruitment Dry Run",
                "active_module": "recruitment"
            }
            render_to_string(template, context)
            success_count += 1
        except Exception as e:
            failed.append((template, str(e)))

    print(f"\n--- RENDER TEST RESULTS ---")
    print(f"Success: {success_count}/{total} ({(success_count/total)*100:.1f}%)")
    
    if failed:
        print(f"Failed: {len(failed)}")
        for tmpl, err in failed:
            print(f"  [x] {tmpl}: {err}")
    else:
        print("All recruitment templates successfully rendered!")

if __name__ == "__main__":
    test_all_recruitment_templates()
