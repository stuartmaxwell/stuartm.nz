"""djpress views file."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from djpress.models import Category, Post


def index(request: HttpRequest) -> HttpResponse:
    """View for the index page."""
    posts = Post.post_objects.get_recent_published_content()

    return render(
        request,
        "djpress/index.html",
        {"posts": posts},
    )


def content_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """View for a single content page."""
    try:
        post = Post.post_objects.get_published_post_by_slug(slug)
    except ValueError as exc:
        msg = "Post not found"
        raise Http404(msg) from exc

    return render(
        request,
        "djpress/index.html",
        {"post": post},
    )


def category_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """View for posts by category."""
    try:
        category: Category = Category.objects.get_category_by_slug(slug=slug)
    except ValueError as exc:
        msg = "Category not found"
        raise Http404(msg) from exc

    posts = Post.post_objects.get_published_content_by_category(category)

    return render(
        request,
        "djpress/index.html",
        {"posts": posts, "category": category},
    )
