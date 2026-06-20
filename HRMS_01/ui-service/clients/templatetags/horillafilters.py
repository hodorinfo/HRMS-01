from django import template

register = template.Library()

# Add any filters if they are used in templates
@register.filter(name="string_to_date")
def string_to_date(value):
    return value
