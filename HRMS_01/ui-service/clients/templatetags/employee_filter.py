from datetime import timedelta
from django import template

register = template.Library()

@register.filter(name="employee_filter")
def employee_filter(value):
    """Stub for generic employee filter."""
    return value

@register.filter(name="shift_status")
def shift_status(value):
    """Stub for shift status."""
    return "Unknown"

@register.filter(name="manager")
def manager(value):
    """Stub for manager."""
    return "Unknown"

@register.filter(name="add_days")
def add_days(value, days):
    if value is not None:
        try:
            return value + timedelta(days=days)
        except Exception:
            return value
    return None

@register.filter(name="edit_accessibility")
def edit_accessibility(emp):
    return True

@register.filter(name="fk_history")
def fk_history(value, arg=None):
    return value

@register.filter(name="currency_symbol_position")
def currency_symbol_position(value, arg=None):
    return f"${value}" if value else ""

