"""Template tags for djpress."""

from django import template
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    return settings.BLOG_TITLE


@register.simple_tag
def post_author_link(post: Post, link_class: str = "") -> str:
    """Return the author link for a post."""
    if not settings.AUTHOR_PATH_ENABLED:
        return post.author_display_name

    author_url = reverse("djpress:author_posts", args=[post.author])

    link_class_html = f' class="{link_class}"' if link_class else ""

    output = (
        f'<a href="{author_url}" title="View all posts by '
        f'{ post.author_display_name }"{link_class_html}>'
        f"{ post.author_display_name }</a>"
    )

    return mark_safe(output)


@register.simple_tag
def post_category_link(category: Category, link_class: str = "") -> str:
    """Return the category links for a post."""
    if not settings.CATEGORY_PATH_ENABLED:
        return category.name

    category_url = reverse("djpress:category_posts", args=[category.slug])

    link_class_html = f' class="{link_class}"' if link_class else ""

    output = (
        f'<a href="{category_url}" title="View all posts in the {category.name} '
        f'category"{link_class_html}>{ category.name }</a>'
    )

    return mark_safe(output)
