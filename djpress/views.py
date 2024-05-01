"""djpress views file."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Category, Content


def index(request: HttpRequest) -> HttpResponse:
    """View for the index page."""
    posts = Content.post_objects.get_recent_published_content()

    return render(
        request,
        "djpress/index.html",
        {"posts": posts},
    )


def content_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """View for a single content page."""
    post = Content.post_objects.get_published_post_by_slug(slug)

    return render(
        request,
        "djpress/index.html",
        {"post": post},
    )


def category_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """View for posts by category."""
    try:
        category: Category = Category.objects.get_category_by_slug(slug=slug)
    except Category.DoesNotExist as exc:
        msg = "Category not found"
        raise Http404(msg) from exc

    posts = Content.post_objects.get_published_content_by_category(category)

    return render(
        request,
        "djpress/index.html",
        {"posts": posts, "category": category},
    )
