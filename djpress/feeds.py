"""RSS feed for blog posts."""

from typing import TYPE_CHECKING

from django.contrib.syndication.views import Feed
from django.urls import reverse

from djpress.models import Content

if TYPE_CHECKING:
    from django.db import models


class ContentFeed(Feed):
    """RSS feed for blog posts."""

    title = "stuartm.nz"
    link = "/rss"
    description = "stuartm.nz updates"

    def items(self: "ContentFeed") -> "models.QuerySet":
        """Return the most recent posts."""
        return Content.get_published_posts()

    def item_title(self: "ContentFeed", item: Content) -> str:
        """Return the title of the post."""
        return item.title

    def item_description(self: "ContentFeed", item: Content) -> str:
        """Return the description of the post."""
        return item.truncated_content_markdown

    def item_link(self: "ContentFeed", item: Content) -> str:
        """Return the link to the post."""
        return reverse("djpress:post_detail", args=[item.slug])
