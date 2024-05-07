"""djpress views file."""

import logging

from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from djpress.models import Category, Post

logger = logging.getLogger(__name__)


def index(
    request: HttpRequest,
) -> HttpResponse:
    """View for the index page."""
    posts = Post.post_objects.get_recent_published_posts()

    return render(
        request,
        "djpress/index.html",
        {"posts": posts},
    )


def date_archives(
    request: HttpRequest,
    year: str = "",
    month: str = "",
    day: str = "",
) -> HttpResponse:
    """View for the date archives pages.

    Args:
        request (HttpRequest): The request object.
        year (int): The year to filter by.
        month (int): The month to filter by.
        day (int): The day to filter by.
    """
    posts = Post.post_objects._get_published_posts()  # noqa: SLF001

    if day:
        logger.debug(f"{year}/{month}/{day}")
        posts = posts.filter(date__year=year, date__month=month, date__day=day)

    elif month:
        logger.debug(f"{year}/{month}")
        posts = posts.filter(date__year=year, date__month=month)

    elif year:
        logger.debug(f"{year}")
        posts = posts.filter(date__year=year)

    return render(
        request,
        "djpress/index.html",
        {"posts": posts},
    )


def post_detail(request: HttpRequest, path: str) -> HttpResponse:
    """View for a single post.

    Args:
        request (HttpRequest): The request object.
        path (str): The path to the post.
    """
    try:
        post = Post.post_objects.get_published_post_by_path(path)
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

    posts = Post.post_objects.get_published_posts_by_category(category)

    return render(
        request,
        "djpress/index.html",
        {"posts": posts, "category": category},
    )


def author_posts(request: HttpRequest, author: str) -> HttpResponse:
    """View for posts by author."""
    try:
        user = User.objects.get(username=author)
    except User.DoesNotExist as exc:
        msg = "Author not found"
        raise Http404(msg) from exc

    posts = Post.post_objects.get_published_posts_by_author(user)

    return render(
        request,
        "djpress/index.html",
        {"posts": posts, "author": author},
    )
