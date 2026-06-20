"""
recruitment_views.py

Generic BFF view handler for all 80+ recruitment module routes.
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
    "pipeline-search/":              "recruitment/pipeline/pipeline.html",
    "pipeline-card":                 "recruitment/pipeline/pipeline.html",
    
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
    "application-form":              "recruitment/candidate/success.html",
    "candidate-self-tracking":       "recruitment/candidate/candidate_self_tracking.html",
    "candidate-login":               "recruitment/candidate/self_login.html",
    "candidate-self-status-tracking/": "recruitment/candidate/candidate_self_tracking.html",

    # ── Interviews ───────────────────────────────────────────────────────
    "interview":                     "recruitment/candidate/interview_view.html",
    "interview/":                    "recruitment/candidate/interview_view.html",
    "interview-view":                "recruitment/candidate/interview_view.html",
    "interview-filter-view":         "recruitment/candidate/interview_list.html",
    "create-interview-schedule":     "recruitment/pipeline/pipeline_components/schedule_interview.html",

    # ── Stages ───────────────────────────────────────────────────────────
    "stages":                        "recruitment/stage/stage_view.html",
    "stages/":                       "recruitment/stage/stage_view.html",
    "stage-view":                    "recruitment/stage/stage_view.html",
    "stage-create":                  "recruitment/stage/stage_form.html",
    "stage-search":                  "recruitment/stage/stage_view.html",
    "add-candidate-to-stage":        "recruitment/candidate/candidate_create_form.html",

    # ── Skill Zones ──────────────────────────────────────────────────────
    "skill-zone":                    "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone/":                   "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone-view":               "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone-create":             "recruitment/skill_zone/skill_zone_form.html",
    "skill-zone-filter":             "recruitment/skill_zone/skill_zone_view.html",
    "skill-zone-cand-filter":        "recruitment/skill_zone_cand/skill_zone_cand_card.html",

    # ── Surveys ──────────────────────────────────────────────────────────
    "survey":                        "recruitment/survey/view_question_templates.html",
    "survey/":                       "recruitment/survey/view_question_templates.html",
    "recruitment-survey-question-template-view": "recruitment/survey/view_question_templates.html",
    "recruitment-survey-question-template-create": "recruitment/survey/template_form.html",
    "survey-template-preview":       "recruitment/survey/survey_preview.html",
    "survey-template-preview/":      "recruitment/survey/survey_preview.html",
    "candidate-survey":              "recruitment/survey/candidate_survey_form.html",
    "filter-survey":                 "recruitment/survey/survey_card.html",
    "recruitment-application-survey":"recruitment/survey/form.html",
    "survey-template-create":        "recruitment/survey/main_form.html",
    "survey-template-question-add":  "recruitment/survey/add_form.html",

    # ── Settings ─────────────────────────────────────────────────────────
    "settings":                      "recruitment/settings/settings.html",
    "create-reject-reason":          "recruitment/settings/reject_reason_form.html",
    "skills-view":                   "recruitment/settings/skills/skills_view.html",
    "create-skills":                 "recruitment/settings/skills/skills_form.html",
    "candidate-reject-reasons":      "recruitment/settings/reject_reasons.html",
    "self-tracking-feature":         "recruitment/settings/settings.html",

    # ── Offer Letters ────────────────────────────────────────────────────
    "offerletter-view":              "recruitment/offerletter/view_letter.html",
    "create-offerletter":            "recruitment/offerletter/create_letter.html",

    # ── Bulk Resumes ─────────────────────────────────────────────────────
    "add-bulk-resume":               "recruitment/pipeline/bulk_resume.html",
    "view-bulk-resume":              "recruitment/pipeline/bulk_resume.html",

    # ── Documents ────────────────────────────────────────────────────────
    "candidate-document-request":    "documents/document_request_create_form.html",
}

# Dynamic routes (path prefix → template) for paths with IDs
DYNAMIC_ROUTE_MAP = [
    # Candidates
    ("candidate-view/",              "recruitment/candidate/individual.html"),
    ("candidate-update/",            "recruitment/candidate/candidate_update_form.html"),
    ("candidate-history/",           "recruitment/candidate/candidate_history.html"),
    ("candidate-stage-update/",      "recruitment/candidate/candidate_update_form.html"),
    ("candidate-document-create/",   "recruitment/candidate/document_create_form.html"),
    ("candidate-file-upload/",       "recruitment/candidate/document_form.html"),
    ("candidate-view-file/",         "recruitment/candidate/view_file.html"),
    ("candidate-add-notes/",         "recruitment/candidate/candidate_self_tracking.html"),
    ("candidate-self-status-tracking/", "recruitment/candidate/candidate_self_tracking.html"),
    ("candidate-document-reject/",   "recruitment/candidate/reject_form.html"),
    
    # Notes / Pipeline Components
    ("view-note/",                   "recruitment/pipeline/pipeline_components/view_note.html"),
    ("add-note/",                    "recruitment/pipeline/pipeline_components/add_note.html"),
    ("create-note/",                 "recruitment/pipeline/pipeline_components/create_note.html"),
    ("note-update/",                 "recruitment/pipeline/pipeline_components/update_note.html"),
    ("note-update-individual/",      "recruitment/pipeline/pipeline_components/update_note.html"),
    ("send-mail/",                   "recruitment/pipeline/pipeline_components/send_mail.html"),
    ("interview-schedule/",          "recruitment/pipeline/pipeline_components/schedule_interview.html"),
    ("edit-interview/",              "recruitment/pipeline/pipeline_components/schedule_interview_update.html"),
    
    # Stages
    ("stage-update/",                "recruitment/stage/stage_update_form.html"),
    ("stage-data/",                  "recruitment/stage/stage_view.html"),
    ("stage-update-pipeline/",       "recruitment/stage/stage_update_form.html"),
    ("stage-title-update/",          "recruitment/stage/stage_update_form.html"),
    ("rec-stage-duplicate/",         "recruitment/stage/stage_form.html"),
    
    # Skill Zones
    ("skill-zone-update/",           "recruitment/skill_zone/skill_zone_form.html"),
    ("skill-zone-cand-create/",      "recruitment/skill_zone_cand/skill_zone_cand_form.html"),
    ("skill-zone-cand-edit/",        "recruitment/skill_zone_cand/skill_zone_cand_form.html"),
    ("skill-zone-cand-card-view/",   "recruitment/skill_zone_cand/skill_zone_cand_card.html"),
    
    # Recruitments
    ("recruitment-update/",          "recruitment/recruitment_update_form.html"),
    ("recruitment-details/",         "recruitment/recruitment_details.html"),
    ("recruitment-duplicate/",       "recruitment/recruitment_duplicate_form.html"),
    ("recruitment-update-pipeline/", "recruitment/recruitment_update_form.html"),
    ("recruitment-archive/",         "recruitment/recruitment_view.html"),
    ("recruitment-stage-get/",       "recruitment/stage/stage_view.html"),
    
    # Surveys
    ("recruitment-survey-question-template-edit/", "recruitment/survey/template_update_form.html"),
    ("recruitment-survey-question-template-delete/", "recruitment/survey/view_question_templates.html"),
    ("recruitment-survey-question-template-duplicate/", "recruitment/survey/template_form.html"),
    ("single-survey-view/",          "recruitment/survey/view_single_template.html"),
    ("survey-template-preview/",     "recruitment/survey/survey_preview.html"),
    
    # Other
    ("pipeline-stages-component/",   "recruitment/pipeline/pipeline.html"),
    ("matching-resumes/",            "recruitment/pipeline/matching_resumes.html"),
    ("add-more-files/",              "recruitment/candidate/document.html"),
    ("add-more-files-individual/",   "recruitment/candidate/document.html"),
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
