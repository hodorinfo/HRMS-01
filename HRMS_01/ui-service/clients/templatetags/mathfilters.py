"""
mathfilters.py

Basic math template filters for the UI service.
"""
from django import template

register = template.Library()


@register.filter(name="add")
def add(value, arg):
    try:
        return float(value) + float(arg)
    except Exception:
        return value


@register.filter(name="sub")
def sub(value, arg):
    try:
        return float(value) - float(arg)
    except Exception:
        return value


@register.filter(name="mul")
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except Exception:
        return value


@register.filter(name="div")
def div(value, arg):
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except Exception:
        return value


@register.filter(name="intdiv")
def intdiv(value, arg):
    try:
        if int(arg) == 0:
            return 0
        return int(value) // int(arg)
    except Exception:
        return value


@register.filter(name="mod")
def mod(value, arg):
    try:
        return int(value) % int(arg)
    except Exception:
        return value
