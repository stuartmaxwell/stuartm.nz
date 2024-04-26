"""djpress models file."""

from typing import ClassVar

import markdown
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self: "Category") -> str:
        """Return the string representation of the category."""
        return self.name


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

    @classmethod
    def get_published_posts(cls: type["Content"]) -> models.QuerySet:
        """Return all published posts.

        Must have a date less than or equal to the current date/time, ordered by date in
        descending order.
        """
        return cls.objects.filter(
            status="published",
            content_type="post",
            date__lte=timezone.now(),
        ).order_by("-date")

    @classmethod
    def get_published_post_by_slug(cls: type["Content"], slug: str) -> "Content":
        """Return a single published post.

        Must have a date less than or equal to the current date/time based on its slug.
        """
        return cls.objects.get(
            slug=slug,
            status="published",
            content_type="post",
            date__lte=timezone.now(),
        )

    @classmethod
    def get_published_posts_by_category(
        cls: type["Content"],
        category: Category,
    ) -> models.QuerySet:
        """Return all published posts.

        Must have a date less than or equal to the current date/time for a specific
        category, ordered by date in descending order.
        """
        return cls.get_published_posts().filter(categories=category)

    def render_markdown(self: "Content", markdown_text: str) -> str:
        """Return the markdown text as HTML."""
        return markdown.markdown(
            markdown_text,
            extensions=["fenced_code", "codehilite"],
            output_format="html",
        )

    @property
    def content_markdown(self: "Content") -> str:
        """Return the content as HTML converted from Markdown."""
        return self.render_markdown(self.content)

    @property
    def truncated_content_markdown(self: "Content") -> str:
        """Return the truncated content as HTML converted from Markdown."""
        read_more_index = self.content.find("<!--more-->")
        if read_more_index != -1:
            truncated_content = self.content[:read_more_index]
        else:
            truncated_content = self.content
        return self.render_markdown(truncated_content)
