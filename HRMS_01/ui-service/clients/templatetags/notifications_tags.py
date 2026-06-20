from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(name="notifications_unread")
def notifications_unread():
    return 0

@register.simple_tag(name="live_notify_badge")
def live_notify_badge():
    return mark_safe('<span class="live_notify_badge">0</span>')

@register.simple_tag(name="register_notify_callbacks")
def register_notify_callbacks(callbacks=None):
    return mark_safe('<script>// Stubbed notify callbacks</script>')
