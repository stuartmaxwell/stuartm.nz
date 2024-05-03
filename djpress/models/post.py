"""Post model."""

import logging
from typing import ClassVar

import markdown
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from config.settings import (
    CACHE_RECENT_PUBLISHED_POSTS,
    MARKDOWN_EXTENSIONS,
    RECENT_PUBLISHED_POSTS_COUNT,
    TRUNCATE_TAG,
)
from djpress.models import Category

logger = logging.getLogger(__name__)

md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS, output_format="html")

PUBLISHED_CONTENT_CACHE_KEY = "published_content"


class PostsManager(models.Manager):
    """Post custom manager."""

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
    ) -> "Post":
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
            except Post.DoesNotExist as exc:
                msg = "Post not found"
                raise ValueError(msg) from exc

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


class Post(models.Model):
    """Post model."""

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

    class Meta:
        """Meta options for the content model."""

        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self: "Post") -> str:
        """Return the string representation of the content."""
        return self.title

    def save(self: "Post", *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Override the save method to auto-generate the slug."""
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug or self.slug.strip("-") == "":
                msg = "Invalid title. Unable to generate a valid slug."
                raise ValueError(msg)
        super().save(*args, **kwargs)

    def render_markdown(self: "Post", markdown_text: str) -> str:
        """Return the markdown text as HTML."""
        html = md.convert(markdown_text)
        logger.debug(f"Converted markdown to HTML: {html=}")
        md.reset()

        return html

    @property
    def content_markdown(self: "Post") -> str:
        """Return the content as HTML converted from Markdown."""
        return self.render_markdown(self.content)

    @property
    def truncated_content_markdown(self: "Post") -> str:
        """Return the truncated content as HTML converted from Markdown."""
        read_more_index = self.content.find(TRUNCATE_TAG)
        if read_more_index != -1:
            truncated_content = self.content[:read_more_index]
        else:
            truncated_content = self.content
        return self.render_markdown(truncated_content)

    @property
    def is_truncated(self: "Post") -> bool:
        """Return whether the content is truncated."""
        return TRUNCATE_TAG in self.content
