"""Template tags for djpress."""

from django import template
from django.db import models

from config.settings import BLOG_TITLE
from djpress.models import Category, Post

register = template.Library()


@register.simple_tag
def get_categories() -> models.QuerySet[Category] | None:
    """Return all categories."""
    return Category.objects.get_categories()


@register.simple_tag
def get_recent_published_posts() -> models.QuerySet[Category] | None:
    """Return recent published posts from the cache."""
    return Post.post_objects.get_recent_published_posts()


@register.simple_tag
def get_single_published_post(slug: str) -> Post | None:
    """Return a single published post by slug."""
    return Post.post_objects.get_published_post_by_slug(slug)


@register.simple_tag
def get_blog_title() -> str:
    """Return the blog title."""
    return BLOG_TITLE
