"""Admin configuration for the SPF Generator app."""

from typing import ClassVar

from django.contrib import admin
from django.utils.html import format_html

from .models import EmailProvider


@admin.register(EmailProvider)
class EmailProviderAdmin(admin.ModelAdmin):
    """Admin interface configuration for EmailProvider model."""

    # pyrefly: ignore [bad-override]
    list_display: ClassVar = [
        "name",
        "category",
        "mechanism_display",
        "lookup_count",
        "priority",
        "active",
    ]

    # pyrefly: ignore [bad-override]
    list_filter: ClassVar = [
        "category",
        "active",
        "mechanism_type",
    ]

    # pyrefly: ignore [bad-override]
    search_fields: ClassVar = [
        "name",
        "description",
        "mechanism_value",
        "notes",
    ]

    # pyrefly: ignore [bad-override]
    readonly_fields: ClassVar = [
        "created_at",
        "updated_at",
    ]

    # pyrefly: ignore [bad-override]
    fieldsets: ClassVar = [
        (
            None,
            {
                "fields": [
                    "name",
                    "category",
                    "description",
                ],
            },
        ),
        (
            "SPF Configuration",
            {
                "fields": [
                    "mechanism_type",
                    "mechanism_value",
                    "lookup_count",
                    "priority",
                ],
            },
        ),
        (
            "Status",
            {
                "fields": [
                    "active",
                    "notes",
                ],
            },
        ),
        (
            "Metadata",
            {
                "classes": ["collapse"],
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]

    @admin.display(description="Mechanism")
    def mechanism_display(self, obj: EmailProvider) -> str:
        """Displays the complete SPF mechanism in the list view.

        Args:
            obj: The EmailProvider instance

        Returns:
            str: HTML-formatted SPF mechanism
        """
        # pyrefly: ignore [bad-return]
        return format_html(
            "<code>{}</code>",
            obj.get_mechanism(),
        )
