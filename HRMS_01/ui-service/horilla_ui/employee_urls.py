"""employee_urls.py — BFF URL router for the Employee module."""
from django.urls import path, re_path
from clients import employee_views

urlpatterns = [
    # Catch-all: every /employee/<anything>/ goes to the generic handler
    re_path(r'^(?P<route>.*)$', employee_views.generic_employee_view, name='employee_generic'),
]
