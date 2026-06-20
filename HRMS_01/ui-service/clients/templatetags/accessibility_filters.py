from django import template

register = template.Library()

@register.filter(name="accessibility_filters")
def accessibility_filters(value):
    return value
