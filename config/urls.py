"""URL configuration for config project."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

urlpatterns += [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path(f"{settings.DJPRESS_ADMIN_PATH}/", include("djpress_admin.urls")),
    path("", include("djpress.urls")),
]
