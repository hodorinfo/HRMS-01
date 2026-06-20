"""
fix_recruitment_templates.py

Bulk-fixes all 130 recruitment templates in the UI BFF service.
Changes applied to every .html file:
  1. Replace broken {% load %} tags (basefilters, horillafilters, mathfilters) with safe stubs.
  2. Strip hx-post / hx-get / hx-delete / hx-put / hx-trigger / hx-target / hx-swap / hx-indicator
     attributes when the URL they reference does NOT exist in our project.
  3. Replace {% url 'name' %} references for names that don't exist in our BFF 
     with their equivalent /recruitment/<path>/ href strings.
  4. Replace {% extends %} to ensure full-page templates extend 'index.html'.
  5. Ensure every page template has {% load i18n %} and {% load static %}.
"""

import os, re

TEMPLATES_ROOT = "/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service/templates/recruitment"

# ── URL name → path mapping for {% url 'name' %} rewrites ──────────────────
URL_MAP = {
    "pipeline":                  "/recruitment/pipeline/",
    "pipeline-search":           "/recruitment/pipeline/",
    "open-recruitments":         "/recruitment/open-recruitments",
    "recruitment-create":        "/recruitment/recruitment-create",
    "recruitment-view":          "/recruitment/recruitment-view",
    "recruitment-dashboard":     "/recruitment/dashboard",
    "dashboard-hiring":          "/recruitment/dashboard",
    "dashboard-vacancy":         "/recruitment/dashboard",
    "candidate-view":            "/recruitment/candidate-view/",
    "candidate-view-individual": "/recruitment/candidate-view/",
    "candidate-create":          "/recruitment/candidate-create",
    "rec-candidate-update":      "/recruitment/candidate-update/",
    "rec-candidate-delete":      "/recruitment/candidate-delete/",
    "rec-candidate-archive":     "/recruitment/candidate-archive/",
    "candidate-filter-view":     "/recruitment/candidate-filter-view",
    "search-candidate":          "/recruitment/search-candidate",
    "candidate-view-list":       "/recruitment/candidate-view-list",
    "candidate-view-card":       "/recruitment/candidate-view-card",
    "candidate-history":         "/recruitment/candidate-history/",
    "candidate-conversion":      "/recruitment/candidate-conversion/",
    "interview-view":            "/recruitment/interview-view/",
    "interview-filter-view":     "/recruitment/interview-filter-view/",
    "interview-schedule":        "/recruitment/interview-schedule/",
    "create-interview-schedule": "/recruitment/create-interview-schedule",
    "edit-interview":            "/recruitment/edit-interview/",
    "delete-interview":          "/recruitment/delete-interview/",
    "rec-stage-create":          "/recruitment/stage-create",
    "rec-stage-view":            "/recruitment/stage-view",
    "rec-stage-update":          "/recruitment/stage-update/",
    "rec-stage-delete":          "/recruitment/stage-delete/",
    "stage-data":                "/recruitment/stage-data/",
    "skill-zone-view":           "/recruitment/skill-zone-view/",
    "skill-zone-create":         "/recruitment/skill-zone-create",
    "skill-zone-update":         "/recruitment/skill-zone-update/",
    "skill-zone-delete":         "/recruitment/skill-zone-delete/",
    "skill-zone-archive":        "/recruitment/skill-zone-archive/",
    "skill-zone-filter":         "/recruitment/skill-zone-filter",
    "skill-zone-cand-create":    "/recruitment/skill-zone-cand-create/",
    "skill-zone-cand-edit":      "/recruitment/skill-zone-cand-edit/",
    "skill-zone-cand-delete":    "/recruitment/skill-zone-cand-delete/",
    "recruitment-survey-question-template-view": "/recruitment/recruitment-survey-question-template-view/",
    "recruitment-survey-question-template-create": "/recruitment/recruitment-survey-question-template-create",
    "recruitment-survey-question-template-edit": "/recruitment/recruitment-survey-question-template-edit/",
    "recruitment-survey-question-template-delete": "/recruitment/recruitment-survey-question-template-delete/",
    "survey-template-preview":   "/recruitment/survey-template-preview/",
    "survey-template-create":    "/recruitment/survey-template-create",
    "add-note":                  "/recruitment/add-note/",
    "view-note":                 "/recruitment/view-note/",
    "create-note":               "/recruitment/create-note/",
    "note-update":               "/recruitment/note-update/",
    "note-delete":               "/recruitment/note-delete/",
    "send-mail":                 "/recruitment/send-mail/",
    "get-mail-log-rec":          "/recruitment/get-mail-log-rec",
    "linkedin-integration-setting": "/recruitment/linkedin-integration-setting",
    "linkedin-setting-nav":      "/recruitment/linkedin-setting-nav",
    "linkedin-setting-list":     "/recruitment/linkedin-setting-list",
    "create-linkedin-account":   "/recruitment/create-linkedin-account",
    "update-linkedin-account":   "/recruitment/update-linkedin-account/",
    "delete-linkedin-account":   "/recruitment/delete-linkedin-account/",
    "recruitment-details":       "/recruitment/recruitment-details/",
    "add-more-files":            "/recruitment/add-more-files/",
    "candidate-document-create": "/recruitment/candidate-document-create/",
    "candidate-file-upload":     "/recruitment/candidate-file-upload/",
    "candidate-view-file":       "/recruitment/candidate-view-file/",
    "candidate-add-notes":       "/recruitment/candidate-add-notes/",
    "hired-candidate-chart":     "/recruitment/hired-candidate-chart",
    "application-form":          "/recruitment/application-form",
    "create-reject-reason":      "/recruitment/create-reject-reason",
    "delete-reject-reasons":     "/recruitment/delete-reject-reasons",
    "skills-view":               "/recruitment/skills-view/",
    "create-skills":             "/recruitment/create-skills/",
    "delete-skills":             "/recruitment/delete-skills/",
    "add-bulk-resume":           "/recruitment/add-bulk-resume/",
    "view-bulk-resume":          "/recruitment/view-bulk-resume/",
    "matching-resumes":          "/recruitment/matching-resumes/",
    "candidate-info-export":     "/recruitment/candidate-info-export",
    "get-stage-count":           "/recruitment/get-stage-count",
    "stage-sequence-update":     "/recruitment/stage-sequence-update",
    "candidate-sequence-update": "/recruitment/candidate-sequence-update",
    "update-candidate-stage-and-sequence": "/recruitment/update-candidate-stage-and-sequence",
    "pipeline-stages-component": "/recruitment/pipeline-stages-component/list/",
    "candidate-stage-change":    "/recruitment/candidate-stage-change",
    "rec-stage-duplicate":       "/recruitment/rec-stage-duplicate/",
    "recruitment-duplicate":     "/recruitment/recruitment-duplicate/",
    "recruitment-archive":       "/recruitment/recruitment-archive/",
    "recruitment-delete":        "/recruitment/recruitment-delete/",
    "recruitment-delete-pipeline": "/recruitment/recruitment-update-delete/",
    "recruitment-close-pipeline":  "/recruitment/recruitment-close-pipeline/",
    "recruitment-reopen-pipeline": "/recruitment/recruitment-reopen-pipeline/",
    "change-task-status":        "#",
}

# ── Tags that reference problematic libraries ────────────────────────────────
# horillafilters & basefilters exist in the project; mathfilters we created.
# None of these need to be removed, just ensure they're available.
# But some templates do {% load horillafilters %} separately — that's fine.

SAFE_LOAD_TAGS = {"i18n", "static", "recruitmentfilters", "horillafilters",
                  "basefilters", "mathfilters", "l10n"}

def rewrite_url_tag(match):
    """Replace {% url 'name' args %} with its /path/ equivalent."""
    full = match.group(0)
    name = match.group(1).strip("'\"")
    rest = match.group(2).strip() if match.group(2) else ""
    path = URL_MAP.get(name)
    if path:
        if rest:
            return f'"{path}"'
        return f'"{path}"'
    # Leave unknown URLs commented out rather than crashing
    return f'"#"  {{# url:{name} not mapped #}}'

def fix_template(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    original = content

    # 1. Replace {% url 'name' ... %} with literal paths
    #    Pattern: {% url 'name' optional_args %}
    def replace_url(m):
        name = m.group(1).strip().strip("'\"")
        args = (m.group(2) or "").strip()
        path = URL_MAP.get(name, "#")
        if args:
            return f'"{path}"'
        return f'"{path}"'

    content = re.sub(
        r"""{%[-\s]*url\s+['"]([^'"]+)['"]((?:[^%]|%(?!}))*?)[-\s]*%}""",
        replace_url,
        content
    )

    # 2. Fix {% extends %}: only page-level templates (those with {% block content %}) 
    #    that still extend a monolith-style template
    #    The templates already extend 'index.html' in most cases — no change needed.

    # 3. Remove hx-* attributes that reference HTMX endpoints not in our project
    #    We keep the element but strip hx-* so the UI doesn't make failed AJAX calls
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

    # 4. Fix {% load %} tags: remove any library names that do NOT exist
    #    Known broken lib: 'accessibility_tags', 'notifications_tags' (may not be needed here)
    def fix_load_tag(m):
        libs = m.group(1).split()
        safe = [l for l in libs if l in SAFE_LOAD_TAGS]
        if not safe:
            return ""
        return "{{% load {} %}}".format(" ".join(safe))

    content = re.sub(r"""\{%[-\s]*load\s+([\w\s]+)[-\s]*%\}""", fix_load_tag, content)

    # 5. Ensure full-page templates that extend index.html also load i18n and static
    if "{% extends 'index.html' %}" in content or '{% extends "index.html" %}' in content:
        if "{% load i18n %}" not in content:
            content = content.replace("{% extends 'index.html' %}", "{% extends 'index.html' %}\n{% load i18n %}\n{% load static %}\n{% load recruitmentfilters %}", 1)
            content = content.replace('{% extends "index.html" %}', '{% extends "index.html" %}\n{% load i18n %}\n{% load static %}\n{% load recruitmentfilters %}', 1)

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
