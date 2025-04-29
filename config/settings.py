"""Django settings for config project."""

from pathlib import Path

import environ
import logfire
import sentry_sdk
from django.contrib.messages import constants as messages
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    SECRET_KEY=(str, "this_is_just_a_temporary_secret_key"),
    DEBUG=(bool, False),
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
    SITE_TITLE=(str, "stuartm.nz"),
    POST_PREFIX=(str, "{{ year }}/{{ month }}"),
    MASTODON_ACCESS_TOKEN=(str, ""),
    RESEND_API_KEY=(str, ""),
    CONTACT_FORM_TO=(str, ""),
    CONTACT_FORM_FROM=(str, ""),
    DEBUGGING_APP_PATH=(str, "this-is-just-a-temporary-debugging-app-path"),
    LOGFIRE_ENVIRONMENT=(str, "dev"),
    BLUESKY_APP_PASSWORD=(str, ""),
    HEALTHCHECK_PATH=(str, ""),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    AWS_ENDPOINT_URL=(str, ""),
    S3_BUCKET=(str, ""),
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
    "django.contrib.sitemaps",
    "djpress.apps.DjpressConfig",
    "storages",
    "healthcheck_app",
    "timezone_converter",
    "markdown_editor",
    "shell",
    "spf_generator",
    "contact_form",
    "home",
    "debugging_app",
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
                "config.context_processors.debug_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
DB_NAME = BASE_DIR / "db" / f"{env('DB_NAME')}.sqlite3" if "sqlite" in env("DB_ENGINE") else env("DB_NAME")
SQLITE_OPTIONS = {
    "init_command": (
        "PRAGMA foreign_keys=ON;"
        "PRAGMA journal_mode = WAL;"
        "PRAGMA synchronous = NORMAL;"
        "PRAGMA busy_timeout = 5000;"
        "PRAGMA temp_store = MEMORY;"
        "PRAGMA mmap_size = 134217728;"
        "PRAGMA journal_size_limit = 67108864;"
        "PRAGMA cache_size = 2000;"
    ),
    "transaction_mode": "IMMEDIATE",
}
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
if "sqlite" in env("DB_ENGINE"):
    DATABASES["default"].update(SQLITE_OPTIONS)

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
    "SITE_TITLE": env("SITE_TITLE"),
    "POST_PREFIX": env("POST_PREFIX"),
    "THEME": "stuartmnz",
    "MARKDOWN_RENDERER": "config.markdown_renderer.mistune_renderer",
    "PLUGINS": [
        "djpress_publish_mastodon",
        "djpress_publish_bluesky",
    ],
    "PLUGIN_SETTINGS": {
        "djpress_publish_mastodon": {
            "instance_url": "https://fosstodon.org",
            "access_token": env("MASTODON_ACCESS_TOKEN"),
            "status_message": "🚀 I created a new blog post!\n\n",
            "base_url": "https://stuartm.nz/",
        },
        "djpress_publish_bluesky": {
            "handle": "stuartm.nz",
            "app_password": env("BLUESKY_APP_PASSWORD"),
            "site_url": "https://stuartm.nz/",
            "post_message": "🚀 I created a new blog post!",
        },
    },
}

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# Contact Form
RESEND_API_KEY = env("RESEND_API_KEY")
CONTACT_FORM_TO = env("CONTACT_FORM_TO")
CONTACT_FORM_FROM = env("CONTACT_FORM_FROM")

# Securtiy settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Use secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Debugging app
DEBUGGING_APP_PATH = env("DEBUGGING_APP_PATH")

# Logfire
LOGFIRE_ENVIRONMENT = env("LOGFIRE_ENVIRONMENT")
logfire.configure(environment=LOGFIRE_ENVIRONMENT)
logfire.instrument_django(
    capture_headers=True,
    excluded_urls="/healthcheck",
)

# Healthcheck app
HEALTHCHECK_PATH = env("HEALTHCHECK_PATH")

# Django Storages
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME
# AWS_ENDPOINT_URL
# S3_BUCKET

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": "stuartmnz-public",
            "endpoint_url": env("AWS_ENDPOINT_URL"),
            "custom_domain": "s.stuartm.nz",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": "stuartmnz-public",
            "endpoint_url": env("AWS_ENDPOINT_URL"),
            "custom_domain": "s.stuartm.nz",
        },
    },
}
