"""Django settings for config project."""

from pathlib import Path

import logfire
import sentry_sdk
from django.contrib.messages import constants as messages
from environs import env
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

# The following line isn't necessary if reading environment variables from memory!
env.read_env()

# set casting, default value
SECRET_KEY = env.str("SECRET_KEY", "this_is_just_a_temporary_secret_key")
DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["127.0.0.1"])
SENTRY_DSN = env.str("SENTRY_DSN", "")
SENTRY_ENVIRONMENT = env.str("SENTRY_ENVIRONMENT", "development")
SENTRY_TRACES_SAMPLE_RATE = env.float("SENTRY_TRACES_SAMPLE_RATE", 0.0)
EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = env.str("EMAIL_PORT", "")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", "")
DB_ENGINE = env.str("DB_ENGINE", "django.db.backends.sqlite3")
DB_NAME = env.str("DB_NAME", "db")
DB_USER = env.str("DB_USER", "")
DB_PASSWORD = env.str("DB_PASSWORD", "")
DB_HOST = env.str("DB_HOST", "")
DB_PORT = env.str("DB_PORT", "")
WHITENOISE_STATIC = env.bool("WHITENOISE_STATIC", False)
ADMIN_URL = env.str("ADMIN_URL", "admin")
SITE_TITLE = env.str("SITE_TITLE", "stuartm.nz")
POST_PREFIX = env.str("POST_PREFIX", "{{ year }}/{{ month }}")
MASTODON_ACCESS_TOKEN = env.str("MASTODON_ACCESS_TOKEN", "")
RESEND_API_KEY = env.str("RESEND_API_KEY", "")
CONTACT_FORM_TO = env.str("CONTACT_FORM_TO", "")
CONTACT_FORM_FROM = env.str("CONTACT_FORM_FROM", "")
DEBUGGING_APP_PATH = env.str("DEBUGGING_APP_PATH", "this-is-just-a-temporary-debugging-app-path")
LOGFIRE_API_KEY = env.str("LOGFIRE_API_KEY", "")
LOGFIRE_ENVIRONMENT = env.str("LOGFIRE_ENVIRONMENT", "dev")
BLUESKY_APP_PASSWORD = env.str("BLUESKY_APP_PASSWORD", "")
HEALTHCHECK_PATH = env.str("HEALTHCHECK_PATH", "")
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", "")
AWS_ENDPOINT_URL = env.str("AWS_ENDPOINT_URL", "")
S3_BUCKET = env.str("S3_BUCKET", "")


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=SENTRY_ENVIRONMENT,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    )

APP_NAME = "stuartm.nz"

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
DB_NAME = BASE_DIR / "db" / f"{DB_NAME}.sqlite3" if "sqlite" in DB_ENGINE else DB_NAME
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
        "ENGINE": DB_ENGINE,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    },
}
if "sqlite" in DB_ENGINE:
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
if LOGFIRE_API_KEY:
    # pyrefly: ignore  # unsupported-operation
    LOGGING["handlers"]["logfire"] = {
        "level": "INFO",
        "class": "logfire.LogfireLoggingHandler",
    }
    # pyrefly: ignore  # index-error, missing-attribute
    LOGGING["root"]["handlers"].append("logfire")


# DJPress settings
DJPRESS_SETTINGS = {
    "SITE_TITLE": SITE_TITLE,
    "POST_PREFIX": POST_PREFIX,
    "THEME": "stuartmnz",
    "MARKDOWN_RENDERER": "config.markdown_renderer.mistune_renderer",
    "PLUGINS": [
        "djpress_publish_mastodon",
        "djpress_publish_bluesky",
    ],
    "PLUGIN_SETTINGS": {
        "djpress_publish_mastodon": {
            "instance_url": "https://fosstodon.org",
            "access_token": MASTODON_ACCESS_TOKEN,
            "status_message": "🚀 I created a new blog post!\n\n",
            "base_url": "https://stuartm.nz/",
            "microblog_category": "microblog",
        },
        "djpress_publish_bluesky": {
            "handle": "stuartm.nz",
            "app_password": BLUESKY_APP_PASSWORD,
            "site_url": "https://stuartm.nz/",
            "post_message": "🚀 I created a new blog post!",
        },
    },
}

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Securtiy settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Use secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logfire
# Logfire
if LOGFIRE_API_KEY:
    logfire.configure(environment=LOGFIRE_ENVIRONMENT, token=LOGFIRE_API_KEY)
    logfire.instrument_django(
        capture_headers=True,
        excluded_urls="/healthcheck",
    )

# Django Storages
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME
# AWS_ENDPOINT_URL
# S3_BUCKET

if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": "stuartmnz-public",
                "endpoint_url": AWS_ENDPOINT_URL,
                "custom_domain": "s.stuartm.nz",
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
