from django import template

register = template.Library()

@register.filter(name="get_histories")
def get_histories(obj):
    return []

@register.filter(name="get_history_values")
def get_history_values(history, field):
    return ""

@register.filter(name="get_diff")
def get_diff(history, previous_history):
    return []
