"""djpress models file."""

import logging
from typing import ClassVar

import markdown
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.http import Http404
from django.utils import timezone
from django.utils.text import slugify

from config.settings import (
    CACHE_CATEGORIES,
    CACHE_RECENT_PUBLISHED_POSTS,
    RECENT_PUBLISHED_POSTS_COUNT,
    TRUNCATE_TAG,
)

logger = logging.getLogger(__name__)

CATEGORY_CACHE_KEY = "categories"
PUBLISHED_CONTENT_CACHE_KEY = "published_content"

markdown_extensions = ["fenced_code", "codehilite"]
md = markdown.Markdown(extensions=markdown_extensions, output_format="html")


class CategoryManager(models.Manager):
    """Category manager."""

    def get_categories(self: "CategoryManager") -> models.QuerySet:
        """Return the queryset for categories.

        If CACHE_CATEGORIES is set to True, we return the cached queryset.
        """
        if CACHE_CATEGORIES:
            return self._get_cached_categories()

        return Category.objects.all()

    def _get_cached_categories(self: "CategoryManager") -> models.QuerySet:
        """Return the cached categories queryset."""
        queryset = cache.get(CATEGORY_CACHE_KEY)

        if queryset is None:
            queryset = Category.objects.all()
            cache.set(CATEGORY_CACHE_KEY, queryset, timeout=None)

        return queryset

    def get_category_by_slug(self: "CategoryManager", slug: str) -> "Category":
        """Return a single category by its slug."""
        # First, try to get the category from the cache
        categories = self.get_categories()
        category = next(
            (category for category in categories if category.slug == slug), None,
        )

        # If the category is not found in the cache, fetch it from the database
        if not category:
            try:
                category = Category.objects.get(slug=slug)
            except Category.DoesNotExist as exc:
                msg = "Category not found"
                # Raise a 404 error
                raise Http404(msg) from exc

        return category


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    # Custom Manager
    objects: "CategoryManager" = CategoryManager()

    def __str__(self: "Category") -> str:
        """Return the string representation of the category."""
        return self.name

    def save(self: "Category", *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Override the save method to auto-generate the slug."""
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug or self.slug.strip("-") == "":
                msg = "Invalid name. Unable to generate a valid slug."
                raise ValueError(msg)
        super().save(*args, **kwargs)


class PostsManager(models.Manager):
    """Content manager."""

    def get_queryset(self: "PostsManager") -> models.QuerySet:
        """Return the queryset for published posts."""
        return super().get_queryset().filter(content_type="post").order_by("-date")

    def _get_published_content(self: "PostsManager") -> models.QuerySet:
        """Returns all published posts.

        For a post to be considered published, it must meet the following requirements:
        - The status must be "published".
        - The date must be less than or equal to the current date/time.
        """
        return self.get_queryset().filter(
            status="published",
            date__lte=timezone.now(),
        )

    def get_recent_published_content(self: "PostsManager") -> models.QuerySet:
        """Return recent published posts.

        If CACHE_RECENT_PUBLISHED_POSTS is set to True, we return the cached queryset.
        """
        if CACHE_RECENT_PUBLISHED_POSTS:
            return self._get_cached_recent_published_content()

        return self._get_published_content().prefetch_related("categories", "author")[
            :RECENT_PUBLISHED_POSTS_COUNT
        ]

    def _get_cached_recent_published_content(self: "PostsManager") -> models.QuerySet:
        """Return the cached recent published posts queryset.

        If there are any future posts, we calculate the seconds until that post, then we
        set the timeout to that number of seconds.
        """
        queryset = cache.get(PUBLISHED_CONTENT_CACHE_KEY)
        logger.debug(f"Getting posts from cache: {queryset=}")

        if queryset is None:
            queryset = (
                self.get_queryset()
                .filter(
                    status="published",
                )
                .prefetch_related("categories", "author")
            )

            future_posts = queryset.filter(date__gt=timezone.now())
            if future_posts.exists():
                future_post = future_posts[0]
                timeout = (future_post.date - timezone.now()).total_seconds()
                logger.debug(f"Future post found, setting timeout to {timeout} seconds")
            else:
                logger.debug("No future posts found, setting timeout to None")
                timeout = None

            queryset = queryset.filter(date__lte=timezone.now())[
                :RECENT_PUBLISHED_POSTS_COUNT
            ]
            logger.debug(f"Setting posts in cache: {queryset=}")
            logger.debug(f"With a timeout of: {timeout=}")
            cache.set(
                PUBLISHED_CONTENT_CACHE_KEY,
                queryset,
                timeout=timeout,
            )

            logger.debug(
                f"Posts set in cache: {cache.get(PUBLISHED_CONTENT_CACHE_KEY)=}",
            )
        return queryset

    def get_published_post_by_slug(
        self: "PostsManager",
        slug: str,
    ) -> "Content":
        """Return a single published post.

        Must have a date less than or equal to the current date/time based on its slug.
        """
        logger.debug(f"Getting post by slug: {slug=}")

        # First, try to get the post from the cache
        posts = self.get_recent_published_content()
        post = next((post for post in posts if post.slug == slug), None)

        # If the post is not found in the cache, fetch it from the database
        if not post:
            try:
                post = self._get_published_content().get(slug=slug)
            except Content.DoesNotExist as exc:
                msg = "Post not found"
                # Raise a 404 error
                raise Http404(msg) from exc

        return post

    def get_published_content_by_category(
        self: "PostsManager",
        category: Category,
    ) -> models.QuerySet:
        """Return all published posts.

        Must have a date less than or equal to the current date/time for a specific
        category, ordered by date in descending order.
        """
        return (
            self._get_published_content()
            .filter(categories=category)
            .prefetch_related("categories", "author")
        )


class Content(models.Model):
    """Content model."""

    STATUS_CHOICES: ClassVar = [("draft", "Draft"), ("published", "Published")]
    CONTENT_TYPE_CHOICES: ClassVar = [("post", "Post"), ("page", "Page")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default="post",
    )
    categories = models.ManyToManyField(Category, blank=True)

    # Managers
    objects = models.Manager()
    post_objects: "PostsManager" = PostsManager()

    def __str__(self: "Content") -> str:
        """Return the string representation of the content."""
        return self.title

    def save(self: "Content", *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Override the save method to auto-generate the slug."""
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug or self.slug.strip("-") == "":
                msg = "Invalid title. Unable to generate a valid slug."
                raise ValueError(msg)
        super().save(*args, **kwargs)

    def render_markdown(self: "Content", markdown_text: str) -> str:
        """Return the markdown text as HTML."""
        html = md.convert(markdown_text)
        logger.debug(f"Converted markdown to HTML: {html=}")
        md.reset()

        return html

    @property
    def content_markdown(self: "Content") -> str:
        """Return the content as HTML converted from Markdown."""
        return self.render_markdown(self.content)

    @property
    def truncated_content_markdown(self: "Content") -> str:
        """Return the truncated content as HTML converted from Markdown."""
        read_more_index = self.content.find(TRUNCATE_TAG)
        if read_more_index != -1:
            truncated_content = self.content[:read_more_index]
        else:
            truncated_content = self.content
        return self.render_markdown(truncated_content)

    @property
    def is_truncated(self: "Content") -> bool:
        """Return whether the content is truncated."""
        return TRUNCATE_TAG in self.content
