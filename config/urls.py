"""URL configuration for config project."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("404", TemplateView.as_view(template_name="404.html")),
        path("500", TemplateView.as_view(template_name="500.html")),
    ]

urlpatterns += [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("contact/", view=include("contact_form.urls")),
    path("utils/timezones/", view=include("timezone_converter.urls")),
    path("utils/markdown-editor/", view=include("markdown_editor.urls")),
    path("utils/spf/", view=include("spf_generator.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("", include("djpress.urls")),
]
