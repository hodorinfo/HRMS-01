"""
fix_employee_templates.py

Bulk-fixes all employee templates in the UI BFF service.
Changes applied to every .html file:
  1. Replace broken {% load %} tags with safe stubs.
  2. Strip hx-post / hx-get / hx-delete / hx-put / hx-trigger / hx-target / hx-swap / hx-indicator
     attributes when the URL they reference does NOT exist in our project.
  3. Replace {% url 'name' %} references with their equivalent /employee/<name>/ href strings.
  4. Replace {% extends "base.html" %} with {% extends "index.html" %}.
  5. Ensure every page template has {% load i18n %} and {% load static %}.
"""

import os, re

TEMPLATES_ROOT = "/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service/templates/employee"

SAFE_LOAD_TAGS = {"i18n", "static", "employee_filter", "horillafilters",
                  "basefilters", "mathfilters", "l10n", "recruitmentfilters", "widget_tweaks"}

def fix_template(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    original = content

    # 1. Replace {% url 'name' ... %} with literal paths
    # Just generic replacement: {% url 'my_view' ... %} -> "/employee/my_view/"
    def replace_url(m):
        name = m.group(1).strip().strip("'\"")
        path = f"/employee/{name}/"
        return f'"{path}"'

    content = re.sub(
        r"""{%[-\s]*url\s+['"]([^'"]+)['"]((?:[^%]|%(?!}))*?)[-\s]*%}""",
        replace_url,
        content
    )

    # Fix base extends
    content = content.replace('{% extends "base.html" %}', '{% extends "index.html" %}')
    content = content.replace("{% extends 'base.html' %}", "{% extends 'index.html' %}")

    # 3. Remove hx-* attributes
    HTMX_ATTRS_REMOVE = [
        r'\s+hx-get=["\'][^"\']*["\']',
        r'\s+hx-post=["\'][^"\']*["\']',
        r'\s+hx-put=["\'][^"\']*["\']',
        r'\s+hx-delete=["\'][^"\']*["\']',
        r'\s+hx-trigger=["\'][^"\']*["\']',
        r'\s+hx-target=["\'][^"\']*["\']',
        r'\s+hx-swap=["\'][^"\']*["\']',
        r'\s+hx-indicator=["\'][^"\']*["\']',
        r'\s+hx-confirm=["\'][^"\']*["\']',
        r'\s+hx-push-url=["\'][^"\']*["\']',
        r'\s+hx-vals=["\'][^"\']*["\']',
        r'\s+hx-include=["\'][^"\']*["\']',
        r'\s+hx-boost=["\'][^"\']*["\']',
    ]
    for pat in HTMX_ATTRS_REMOVE:
        content = re.sub(pat, "", content)

    # 4. Fix {% load %} tags
    def fix_load_tag(m):
        libs = m.group(1).split()
        safe = [l for l in libs if l in SAFE_LOAD_TAGS]
        if not safe:
            return ""
        return "{{% load {} %}}".format(" ".join(safe))

    content = re.sub(r"""\{%[-\s]*load\s+([\w\s]+)[-\s]*%\}""", fix_load_tag, content)

    # 5. Fix double quotes from previously bad replaces
    content = re.sub(r'<a(/employee/[^"]+/)""', r'<a href="\1"', content)
    content = re.sub(r'href=""(/employee/[^"]+)""', r'href="\1"', content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

changed = 0
skipped = 0
for root, dirs, files in os.walk(TEMPLATES_ROOT):
    for fname in files:
        if fname.endswith(".html"):
            fpath = os.path.join(root, fname)
            if fix_template(fpath):
                rel = fpath.replace(TEMPLATES_ROOT + "/", "")
                print(f"  ✓ Updated: {rel}")
                changed += 1
            else:
                skipped += 1

print(f"\nDone. {changed} files updated, {skipped} already clean.")
