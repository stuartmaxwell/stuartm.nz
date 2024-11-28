"""Sitemap for stuartm.nz."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    """Sitemap for stuartm.nz."""

    changefreq = "monthly"
    protocol = "https"

    def items(self) -> list:
        """Return a list of URL names that you want to include."""
        return [
            "timezone_converter:converter",
            "markdown_editor:markdown_editor",
            "spf_generator:spf_generator",
            "home:home",
        ]

    def location(self, item: str) -> str:
        """Generate the URL for each item using Django's reverse."""
        return reverse(item)

    def lastmod(self, _: dict) -> None:
        """Return the last modification time for each item."""
        return
