"""
onboardingfilters.py

This page is used to write custom template filters.
"""

from django import template

register = template.Library()

@register.filter(name="is_taskmanager")
def is_taskmanager(user):
    return True

@register.filter(name="task_manages")
def task_manages(user, recruitment):
    return True

@register.filter(name="stage_manages")
def stage_manages(user, stage):
    return True

@register.filter(name="task_manager")
def task_manager(user, task):
    return True
