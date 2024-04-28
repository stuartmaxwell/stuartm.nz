"""Template tags for djpress."""

from django import template
from django.db import models

from djpress.models import Category

register = template.Library()


@register.simple_tag
def get_categories() -> models.QuerySet[Category] | None:
    """Return all categories."""
    return Category.get_cached_queryset()
