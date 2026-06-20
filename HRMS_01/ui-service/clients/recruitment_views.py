"""
recruitment_views.py

Generic BFF view handler for all 40+ recruitment module routes.
Maps each URL path to the correct template in templates/recruitment/.
"""
from django.shortcuts import render, redirect


def _is_authenticated(request):
    """Use the same auth check as the rest of the BFF views."""
    return bool(request.session.get("access_token"))


# Full route → template map (path after /recruitment/)
ROUTE_TEMPLATE_MAP = {
    # ── Main / Open Recruitments ─────────────────────────────────────────
    "":                              "recruitment/open_recruitments.html",
    "open-recruitments":             "recruitment/open_recruitments.html",
    "open-jobs":                     "recruitment/open_recruitments.html",
    "open-jobs/":                    "recruitment/open_recruitments.html",
    "recruitment-view":              "recruitment/recruitment_view.html",
    "recruitment-create":            "recruitment/recruitment_create.html",

    # ── Pipeline / Kanban ────────────────────────────────────────────────
    "pipeline":                      "recruitment/pipeline/pipeline.html",
    "pipeline/":                     "recruitment/pipeline/pipeline.html",

    # ── Dashboard ────────────────────────────────────────────────────────
    "dashboard":                     "recruitment/dashboard/dashboard.html",

    # ── Candidates ───────────────────────────────────────────────────────
    "candidates":                    "recruitment/candidate/candidate_view.html",
    "candidates/":                   "recruitment/candidate/candidate_view.html",
    "candidate-view":                "recruitment/candidate/candidate_view.html",
    "candidate-create":              "recruitment/candidate/candidate_create_form.html",
    "candidate-view-list":           "recruitment/candidate/candidate_list.html",
    "candidate-view-card":           "recruitment/candidate/candidate_card.html",
    "candidate-filter-view":         "recruitment/candidate/candidate_card.html",
    "search-candidate":              "recruitment/candidate/candidate_card.html",
    "candidate-info-export":         "recruitment/candidate/export_filter.html",
    "application-form":              "recruitment/candidate/application_form.html",
    "candidate-self-tracking":       "recruitment/candidate/candidate_self_tracking.html",

    # ── Interviews ───────────────────────────────────────────────────────
    "interview":                     "recruitment/candidate/interview_view.html",
    "interview/":                    "recruitment/candidate/interview_view.html",
    "interview-view":                "recruitment/candidate/interview_view.html",
    "interview-filter-view":         "recruitment/candidate/interview_view.html",

    # ── Stages ───────────────────────────────────────────────────────────
    "stages":                        "recruitment/stage/stage_view.html",
    "stages/":                       "recruitment/stage/stage_view.html",
    "stage-view":                    "recruitment/stage/stage_view.html",
    "stage-create":                  "recruitment/stage/stage_form.html",

    # ── Skill Zones ──────────────────────────────────────────────────────
    "skill-zone":                    "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone/":                   "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone-view":               "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone-create":             "recruitment/skill_zone/skill_zone_form.html",

    # ── Surveys ──────────────────────────────────────────────────────────
    "survey":                        "recruitment/survey/view_question_templates.html",
    "survey/":                       "recruitment/survey/view_question_templates.html",
    "recruitment-survey-question-template-view": "recruitment/survey/view_question_templates.html",
    "recruitment-survey-question-template-create": "recruitment/survey/template_form.html",
    "survey-template-preview":       "recruitment/survey/survey_preview.html",
    "candidate-survey":              "recruitment/survey/candidate_survey_form.html",
    "filter-survey":                 "recruitment/survey/survey_card.html",

    # ── LinkedIn ─────────────────────────────────────────────────────────
    "linkedin-integration-setting":  "recruitment/linkedin/linkedin_setting.html",
    "linkedin-setting-list":         "recruitment/linkedin/linkedin_setting_list.html",
    "create-linkedin-account":       "recruitment/linkedin/linkedin_setting.html",

    # ── Settings ─────────────────────────────────────────────────────────
    "settings":                      "recruitment/settings/settings.html",
    "create-reject-reason":          "recruitment/settings/settings.html",
    "skills-view":                   "recruitment/settings/settings.html",

    # ── Offer Letters ────────────────────────────────────────────────────
    "offerletter-view":              "recruitment/offerletter/view_letter.html",
    "create-offerletter":            "recruitment/offerletter/create_letter.html",

    # ── Bulk Resumes ─────────────────────────────────────────────────────
    "add-bulk-resume":               "recruitment/pipeline/bulk_resume.html",
    "view-bulk-resume":              "recruitment/pipeline/bulk_resume.html",
}

# Dynamic routes (path prefix → template) for paths with IDs
DYNAMIC_ROUTE_MAP = [
    ("candidate-view/",              "recruitment/candidate/individual.html"),
    ("candidate-update/",            "recruitment/candidate/candidate_update_form.html"),
    ("candidate-history/",           "recruitment/candidate/history.html"),
    ("candidate-stage-update/",      "recruitment/candidate/candidate_update_form.html"),
    ("candidate-document-create/",   "recruitment/candidate/document_create_form.html"),
    ("candidate-file-upload/",       "recruitment/candidate/document_form.html"),
    ("candidate-view-file/",         "recruitment/candidate/view_file.html"),
    ("candidate-add-notes/",         "recruitment/candidate/individual.html"),
    ("view-note/",                   "recruitment/pipeline/pipeline_components/view_note.html"),
    ("add-note/",                    "recruitment/pipeline/pipeline_components/add_note.html"),
    ("create-note/",                 "recruitment/pipeline/pipeline_components/create_note.html"),
    ("note-update/",                 "recruitment/pipeline/pipeline_components/update_note.html"),
    ("send-mail/",                   "recruitment/pipeline/pipeline_components/send_mail.html"),
    ("interview-schedule/",          "recruitment/pipeline/pipeline_components/schedule_interview.html"),
    ("edit-interview/",              "recruitment/pipeline/pipeline_components/schedule_interview_update.html"),
    ("stage-update/",                "recruitment/stage/stage_update_form.html"),
    ("stage-data/",                  "recruitment/stage/stage_view.html"),
    ("skill-zone-update/",           "recruitment/skill_zone/skill_zone_form.html"),
    ("skill-zone-cand-create/",      "recruitment/skill_zone_cand/skill_zone_cand_form.html"),
    ("skill-zone-cand-edit/",        "recruitment/skill_zone_cand/skill_zone_cand_form.html"),
    ("skill-zone-cand-card-view/",   "recruitment/skill_zone_cand/skill_zone_cand_card.html"),
    ("recruitment-update/",          "recruitment/recruitment_update_form.html"),
    ("recruitment-details/",         "recruitment/recruitment_details.html"),
    ("recruitment-duplicate/",       "recruitment/recruitment_duplicate_form.html"),
    ("recruitment-survey-question-template-edit/", "recruitment/survey/template_update_form.html"),
    ("recruitment-survey-question-template-delete/", "recruitment/survey/view_question_templates.html"),
    ("single-survey-view/",          "recruitment/survey/view_single_template.html"),
    ("update-linkedin-account/",     "recruitment/linkedin/linkedin_setting.html"),
    ("delete-linkedin-account/",     "recruitment/linkedin/linkedin_setting_list.html"),
    ("pipeline-stages-component/",   "recruitment/pipeline/pipeline.html"),
    ("matching-resumes/",            "recruitment/pipeline/matching_resumes.html"),
    ("add-more-files/",              "recruitment/candidate/document.html"),
]


def generic_recruitment_view(request, route=""):
    """Route all /recruitment/<route>/ paths to their templates."""
    if not _is_authenticated(request):
        return redirect("login")
    # Normalize trailing slash
    route = route.strip("/")

    # 1. Exact match
    if route in ROUTE_TEMPLATE_MAP:
        template = ROUTE_TEMPLATE_MAP[route]
        return render(request, template, _ctx(route))

    # 2. Prefix/dynamic match (route with ID like candidate-view/1)
    for prefix, template in DYNAMIC_ROUTE_MAP:
        if route.startswith(prefix.rstrip("/")):
            return render(request, template, _ctx(route))

    # 3. Fallback
    return render(request, "module_view.html", {
        "page_title": "Recruitment — " + route.replace("-", " ").title(),
        "active_module": "recruitment",
        "breadcrumbs": [
            {"title": "Recruitment", "url": "/recruitment/"},
            {"title": route.replace("-", " ").title(), "url": ""},
        ],
    })


def _ctx(route):
    """Build a minimal template context."""
    return {
        "page_title": route.replace("-", " ").title() if route else "Recruitment",
        "active_module": "recruitment",
    }
