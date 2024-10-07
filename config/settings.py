"""Django settings for config project."""

from pathlib import Path

import environ
import pymdownx.emoji
import sentry_sdk
from django.contrib.messages import constants as messages
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    SECRET_KEY=(str, "this_is_just_a_temporary_secret_key"),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ["127.0.0.1"]),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, "development"),
    SENTRY_TRACES_SAMPLE_RATE=(float, 0.0),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_TLS=(bool, True),
    DEFAULT_FROM_EMAIL=(str, ""),
    DB_ENGINE=(str, "django.db.backends.sqlite3"),
    DB_NAME=(str, "db"),
    DB_USER=(str, ""),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, ""),
    DB_PORT=(str, ""),
    WHITENOISE_STATIC=(bool, False),
    ADMIN_URL=(str, "admin"),
    BLOG_TITLE=(str, "stuartm.nz"),
)

environ.Env.read_env(Path(BASE_DIR / ".env"))

SENTRY_DSN = env("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        environment=str(env("SENTRY_ENVIRONMENT")),
        traces_sample_rate=env("SENTRY_TRACES_SAMPLE_RATE"),
    )

APP_NAME = "stuartm.nz"

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")


ADMIN_URL = env("ADMIN_URL")

CSRF_TRUSTED_ORIGINS = [f"https://{domain}" for domain in ALLOWED_HOSTS]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djpress.apps.DjpressConfig",
    "timezone_converter",
    "markdown_editor",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",  # Required for django-debug-toolbar
    ]

# The middleware section is broken up to allow various middleware to be
# added in different environments and in different orders.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

# Whitenoise
WHITENOISE_STATIC = env("WHITENOISE_STATIC")
if WHITENOISE_STATIC:
    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

# django-debug-toolbar
if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DB_NAME = BASE_DIR / f"{env('DB_NAME')}.sqlite3" if "sqlite" in env("DB_ENGINE") else env("DB_NAME")

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": DB_NAME,
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation.UserAttributeSimilarityValidator"),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-nz"

TIME_ZONE = "Pacific/Auckland"

USE_I18N = True

USE_TZ = True

# The path that the static files will be served from
STATIC_URL = "/static/"
# The directory that collectstatic will collect static files to
STATIC_ROOT = BASE_DIR / "staticfiles"
# The directory that static files will be collected from
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

LOGIN_REDIRECT_URL = "djpress:index"
LOGOUT_REDIRECT_URL = "djpress:index"

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# django-debug-toolbar
INTERNAL_IPS = ["127.0.0.1"]

# The following constants let us use Bootstrap alerts with messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Media uploads for untrusted files
MEDIA_ROOT = "media"
MEDIA_URL = "/media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "filters": ["require_debug_true"],
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": [],
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

# DJPress settings
DJPRESS_SETTINGS = {
    "MARKDOWN_EXTENSIONS": ["pymdownx.superfences", "pymdownx.highlight", "tables", "pymdownx.emoji", "toc"],
    "MARKDOWN_EXTENSION_CONFIGS": {"pymdownx.emo,ji": {"emoji_generator": pymdownx.emoji.to_alt}},
    "BLOG_TITLE": "stuartm.nz",
}
