"""recruitment_urls.py — BFF URL router for the Recruitment module."""
from django.urls import path, re_path
from clients import recruitment_views

urlpatterns = [
    # Catch-all: every /recruitment/<anything>/ goes to the generic handler
    re_path(r'^(?P<route>.*)$', recruitment_views.generic_recruitment_view, name='recruitment_generic'),
]
