"""
recruitmentfilters.py

Custom template filters for the Recruitment module in the UI BFF service.
This is a standalone version that does NOT depend on the recruitment.models
from the monolith — it works with plain Python data objects/dicts.
"""

import json
import uuid

from django import template

register = template.Library()


@register.filter(name="is_stagemanager")
def is_stagemanager(user):
    """Check if user is a stage or recruitment manager (stub for BFF)."""
    return True


@register.filter(name="is_recruitmentmanager")
def is_recruitmentmangers(user):
    """Check if user is a recruitment manager (stub for BFF)."""
    return True


@register.filter(name="stage_manages")
def stage_manages(user, recruitment):
    """Check if user manages any stage in a recruitment (stub for BFF)."""
    return True


@register.filter(name="recruitment_manages")
def recruitment_manages(user, recruitment):
    """Check if user is in recruitment managers (stub for BFF)."""
    return True


@register.filter(name="employee")
def employee_filter(uid):
    """Return a placeholder employee dict for a given user id."""
    return None


@register.filter(name="media_path")
def media_path(form_tag):
    """Return the media path from a form widget."""
    try:
        return form_tag.subwidgets[0].__dict__["data"]["value"]
    except Exception:
        return ""


@register.filter(name="generate_id")
def generate_id(element, label=""):
    """Generate a unique id attr for a form element."""
    try:
        element.field.widget.attrs.update({"id": label + str(uuid.uuid1())})
    except Exception:
        pass
    return element


@register.filter(name="has_candidate_rating")
def has_candidate_rating(candidate_ratings, cand):
    """Check if a candidate has a rating (stub for BFF)."""
    return None


@register.filter(name="rating")
def rating_filter(candidate_ratings, cand):
    """Return a candidate's rating (stub for BFF)."""
    return "0"


@register.filter(name="avg_rating")
def avg_rating(candidate_ratings, cand):
    """Return the average rating of a candidate (stub for BFF)."""
    return "0"


@register.filter(name="percentage")
def percentage(value, total):
    """Convert a value to a percentage of total."""
    try:
        if not total or total == 0:
            return 0
        return min(round((value / total) * 100, 2), 100)
    except Exception:
        return 0


@register.filter(name="is_in_task_managers")
def is_in_task_managers(user):
    """Check if user is in task managers (stub for BFF)."""
    return False


@register.filter(name="pipeline_grouper")
def pipeline_grouper(grouper: dict = {}):
    """Itemize pipeline grouper dictionary."""
    return grouper.get("title", ""), grouper.get("stages", [])


@register.filter(name="to_json")
def to_json(value):
    """Convert stage queryset-like iterable to JSON."""
    try:
        ordered_list = [
            {"id": val.id, "stage": val.stage, "type": val.stage_type} for val in value
        ]
        return json.dumps(ordered_list)
    except Exception:
        return "[]"


@register.filter(name="on_off")
def on_off(value):
    """Convert on/off string to Yes/No."""
    if value == "on":
        return "Yes"
    return "No"


@register.filter(name="mathfilters_add")
def mathfilters_add(value, arg):
    """Add two numbers."""
    try:
        return int(value) + int(arg)
    except Exception:
        return value
