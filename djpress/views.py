"""djpress views file."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Category, Content


def home(request: HttpRequest) -> HttpResponse:
    """View for the home page."""
    posts = Content.get_published_posts()
    return render(request, "djpress/home.html", {"posts": posts})


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """View for a single post page."""
    try:
        post = Content.get_published_post_by_slug(slug)
    except Content.DoesNotExist as exc:
        msg = "Post not found"
        raise Http404(msg) from exc

    return render(request, "djpress/post.html", {"post": post})


def category_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """View for posts by category."""
    try:
        category = Category.objects.get(slug=slug)
        posts = Content.get_published_posts_by_category(category)
    except Category.DoesNotExist as exc:
        msg = "Category not found"
        raise Http404(msg) from exc

    return render(
        request,
        "djpress/category_posts.html",
        {"category": category, "posts": posts},
    )
