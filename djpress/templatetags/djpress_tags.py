"""Template tags for djpress."""

from django import template
from django.db import models

from djpress.models import Category, Content

register = template.Library()


@register.simple_tag
def get_categories() -> models.QuerySet[Category] | None:
    """Return all categories from the cache."""
    return Category.get_cached_categories()


@register.simple_tag
def get_published_content() -> models.QuerySet[Category] | None:
    """Return all published posts from the cache."""
    return Content.post_objects.get_cached_published_content()


@register.simple_tag
def get_single_published_content(slug: str) -> Content | None:
    """Return a single published post by slug."""
    return Content.post_objects.get_published_post_by_slug(slug)
