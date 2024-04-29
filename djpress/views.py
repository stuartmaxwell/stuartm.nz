"""djpress views file."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Category, Content


def index(request: HttpRequest) -> HttpResponse:
    """View for the index page."""
    return render(request, "djpress/index.html")


def content_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """View for a single content page."""
    return render(request, "djpress/index.html", {"slug": slug})


def category_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """View for posts by category."""
    try:
        category = Category.objects.get(slug=slug)
        posts = Content.post_objects.get_published_content_by_category(category)
    except Category.DoesNotExist as exc:
        msg = "Category not found"
        raise Http404(msg) from exc

    return render(
        request,
        "djpress/category_posts.html",
        {"category": category, "posts": posts},
    )
