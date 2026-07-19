"""URL configuration for config project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from djpress.admin import PostAdmin
from djpress.models import Post
from djpress.sitemaps import (
    CategorySitemap,
    DateBasedSitemap,
    PageSitemap,
    PostSitemap,
)
from djpress_tiptap.widgets import DjTiptapWidget

from config.sitemaps import StaticSitemap

"""Custom admin configuration."""
admin.site.unregister(Post)

@admin.register(Post)
class TiptapPostAdmin(PostAdmin):
    """Over-ride the DJ Press PostAdmin."""
    def get_form(self, request, obj=None, change=False, **kwargs):  # noqa: ANN001, ANN003, ANN201, D102, FBT002
        kwargs["widgets"] = {"content": DjTiptapWidget()}
        return super().get_form(request, obj, change, **kwargs)

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
    path("utils/timezones/", view=include("timezone_converter.urls")),
    path("utils/markdown-editor/", view=include("markdown_editor.urls")),
    path("utils/spf/", view=include("spf_generator.urls")),
    path("utils/home/", view=include("home.urls")),
    path("utils/__debugging__/", view=include("debugging_app.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("media/", include("djpress_tiptap.urls")),
    path("", include("djpress.urls")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
