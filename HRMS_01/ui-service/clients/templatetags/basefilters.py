from django import template
from django.conf import settings

register = template.Library()

@register.filter(name="app_installed")
def app_installed(app_name):
    # Mock apps that are "installed" in the monolith so the BFF templates render correctly
    mock_apps = ["attendance", "base", "leave", "horilla_automations", "payroll", "pms", "recruitment"]
    return app_name in settings.INSTALLED_APPS or app_name in mock_apps


@register.filter(name="feature_is_accessible")
def feature_is_accessible(feature_name, request=None):
    return True

@register.filter(name="is_reportingmanager")
def is_reportingmanager(user):
    return True

@register.filter(name="check_manager")
def check_manager(user, employee):
    return True

@register.filter(name="yes_no")
def yes_no(value):
    return "Yes" if value else "No"

@register.filter(name="abs_value")
def abs_value(value):
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        try:
            return abs(float(value))
        except (ValueError, TypeError):
            return value

@register.filter(name="is_stagemanager")
def is_stagemanager(user):
    return True

@register.filter(name="any_permission")
def any_permission(user, arg=None):
    return True

@register.filter(name="config_perms")
def config_perms(user):
    return True

@register.filter(name="filter_field")
def filter_field(value):
    """Format field name for display"""
    if not value:
        return ""
    return str(value).replace("_", " ").title()

@register.filter(name="base64_encode")
def base64_encode(value):
    return ""

@register.filter(name="fk_history")
def fk_history(value, arg):
    return ""
