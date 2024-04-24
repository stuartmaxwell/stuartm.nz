"""djpress models file."""

from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models


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
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
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

    @classmethod
    def get_published_posts(cls: type["Content"]) -> models.QuerySet:
        """Return all published posts ordered by date."""
        return cls.objects.filter(status="published", content_type="post").order_by(
            "-date",
        )

    @classmethod
    def get_published_post_by_slug(cls: type["Content"], slug: str) -> "Content":
        """Return a single published post based on its slug."""
        return cls.objects.get(slug=slug, status="published", content_type="post")

    @classmethod
    def get_published_posts_by_category(
        cls: type["Content"],
        category: Category,
    ) -> models.QuerySet:
        """Return all published posts for a specific category."""
        return cls.get_published_posts().filter(categories=category)
