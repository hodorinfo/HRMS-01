import os
import re

TEMPLATES_ROOT = "/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service/templates/recruitment"

def clean_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # 1. Remove standard hx- attributes
    hx_attrs = [
        "hx-get", "hx-post", "hx-put", "hx-delete", "hx-patch",
        "hx-target", "hx-swap", "hx-trigger", "hx-include",
        "hx-indicator", "hx-push-url", "hx-confirm", "hx-disable",
        "hx-encoding", "hx-ext", "hx-headers", "hx-history",
        "hx-history-elt", "hx-params", "hx-preserve", "hx-prompt",
        "hx-replace-url", "hx-request", "hx-select", "hx-select-oob",
        "hx-swap-oob", "hx-sync", "hx-validate", "hx-vals", "hx-on"
    ]

    for attr in hx_attrs:
        # Match attr="something" or attr='something'
        pattern = rf'{attr}=["\'](.*?)["\']'
        content = re.sub(pattern, '', content)

    # Clean empty class="" just in case HTMX classes were empty (rare but good for cleanliness)
    content = content.replace('class=""', '')

    # 2. Add specific basefilters for the recruitment module
    if "{% extends 'index.html' %}" in content or '{% extends "index.html" %}' in content:
        if "{% load i18n %}" not in content and "{% load horillafilters" not in content:
            # We must be careful because some templates might have {% extends 'index.html' %} on the same line as other tags
            content = content.replace("{% extends 'index.html' %}", "{% extends 'index.html' %}\n{% load i18n static basefilters horillafilters recruitmentfilters %}", 1)
            content = content.replace('{% extends "index.html" %}', '{% extends "index.html" %}\n{% load i18n static basefilters horillafilters recruitmentfilters %}', 1)

    # If the file uses app_installed but doesn't have basefilters, add it
    if "app_installed" in content and "{% load basefilters" not in content:
        content = "{% load basefilters %}\n" + content

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    updated = 0
    total = 0
    for root, dirs, files in os.walk(TEMPLATES_ROOT):
        for f in files:
            if f.endswith('.html'):
                total += 1
                if clean_file(os.path.join(root, f)):
                    updated += 1
    
    print(f"Sanitization complete. Updated {updated} out of {total} recruitment templates.")

if __name__ == '__main__':
    main()
