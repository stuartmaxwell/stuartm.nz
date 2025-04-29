"""URL configuration for config project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from djpress.sitemaps import (
    CategorySitemap,
    DateBasedSitemap,
    PageSitemap,
    PostSitemap,
)

from config.sitemaps import StaticSitemap

sitemaps = {
    "posts": PostSitemap,
    "pages": PageSitemap,
    "categories": CategorySitemap,
    "archives": DateBasedSitemap,
    "static": StaticSitemap,
}

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("404", TemplateView.as_view(template_name="404.html")),
        path("500", TemplateView.as_view(template_name="500.html")),
    ]

urlpatterns += [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("healthcheck/", view=include("healthcheck_app.urls")),
    path("contact/", view=include("contact_form.urls")),
    path("utils/timezones/", view=include("timezone_converter.urls")),
    path("utils/markdown-editor/", view=include("markdown_editor.urls")),
    path("utils/spf/", view=include("spf_generator.urls")),
    path("utils/home/", view=include("home.urls")),
    path("utils/__debugging__/", view=include("debugging_app.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("djpress.urls")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
