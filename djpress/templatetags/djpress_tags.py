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
    return Content.get_cached_published_content()
