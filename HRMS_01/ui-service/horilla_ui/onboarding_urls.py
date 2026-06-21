from django.urls import path, re_path
from clients import onboarding_views

urlpatterns = [
    # Catch-all: every /onboarding/<anything>/ goes to the generic handler
    re_path(r'^(?P<route>.*)$', onboarding_views.generic_onboarding_view, name='onboarding_generic'),
]
