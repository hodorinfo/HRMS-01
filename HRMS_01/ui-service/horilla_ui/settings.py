"""Django settings for Horilla UI BFF service."""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-django-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "clients",
    "django.contrib.humanize",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "horilla_ui.middleware.JWTSessionMiddleware",
]

ROOT_URLCONF = "horilla_ui.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "local_templates",
            BASE_DIR / "templates",
            BASE_DIR / "templates/employee/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "horilla_ui.context_processors.service_urls",
            ],
            "builtins": [
                "clients.templatetags.url_fallback",
            ],
        },
    },
]

WSGI_APPLICATION = "horilla_ui.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "bff.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# Microservice URLs
IDENTITY_SERVICE_URL = os.environ.get("IDENTITY_SERVICE_URL", "http://identity-service:8000")
CORE_SERVICE_URL = os.environ.get("CORE_SERVICE_URL", "http://core-service:8000")
ATTENDANCE_SERVICE_URL = os.environ.get("ATTENDANCE_SERVICE_URL", "http://attendance-service:8000")
PAYROLL_SERVICE_URL = os.environ.get("PAYROLL_SERVICE_URL", "http://payroll-service:8000")
PERMISSION_SERVICE_URL = os.environ.get("PERMISSION_SERVICE_URL", "http://permission-service:8000")
TALENT_SERVICE_URL = os.environ.get("TALENT_SERVICE_URL", "http://talent-service:8000")
PLATFORM_SERVICE_URL = os.environ.get("PLATFORM_SERVICE_URL", "http://platform-service:8000")

SESSION_ENGINE = "django.contrib.sessions.backends.db"

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:8000,http://localhost"
).split(",")

X_FRAME_OPTIONS = "SAMEORIGIN"

# Disable SSL redirects in dev
SECURE_SSL_REDIRECT = False
