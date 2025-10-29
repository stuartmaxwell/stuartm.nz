"""Models for the spf_generator app."""

from typing import ClassVar

from django.db import models


class SpfAllMechanism(models.TextChoices):
    """SPF 'all' mechanism options.

    FAIL: -all - Explicitly deny all other servers
    SOFTFAIL: ~all - Suggest denial but don't enforce
    NEUTRAL: ?all - Take no position
    """

    FAIL = "-all", "Fail (-all)"
    SOFTFAIL = "~all", "Softfail (~all)"
    NEUTRAL = "?all", "Neutral (?all)"

    @property
    def description(self) -> str:
        """Returns a brief description of what this mechanism does."""
        descriptions = {
            self.FAIL: "explicitly rejects mail from unlisted servers",
            self.SOFTFAIL: "suggests rejection but doesn't enforce it",
            self.NEUTRAL: "takes no position on unlisted servers",
        }
        return descriptions[self]


class ProviderCategory(models.TextChoices):
    """Enumeration of different email provider categories.

    EMAIL_HOSTING: Services that provide email hosting (e.g., Google Workspace, Microsoft 365)
    TRANSACTIONAL: Services for sending automated/transactional emails (e.g., SendGrid, Mailgun)
    """

    EMAIL_HOSTING = "EMAIL_HOSTING", "Email Hosting"
    TRANSACTIONAL = "TRANSACTIONAL", "Transactional Email"
    OTHER = "OTHER", "Other"


class SpfMechanism(models.TextChoices):
    """Enumeration of SPF mechanisms in order of recommended usage.

    The order matters as it affects how SPF records are evaluated.
    """

    INCLUDE = "include", "Include"
    A = "a", "A Record"
    MX = "mx", "MX Record"
    IP4 = "ip4", "IPv4"
    IP6 = "ip6", "IPv6"
    EXISTS = "exists", "Exists"


class EmailProvider(models.Model):
    """Model to store email provider information and their SPF requirements.

    Attributes:
        name (str): Name of the email provider
        category (ProviderCategory): Category of the provider
        description (str): Optional description of the provider
        mechanism_type (SpfMechanism): Type of SPF mechanism used
        mechanism_value (str): The actual SPF record value
        lookup_count (int): Number of DNS lookups this mechanism requires
        priority (int): Order in which this should appear in combined SPF record
        active (bool): Whether this provider is currently available for selection
        notes (str): Optional internal notes about this provider
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the email provider (e.g., 'Google Workspace', 'SendGrid')",
    )

    category = models.CharField(
        max_length=20,
        choices=ProviderCategory,
        help_text="Category of email provider",
    )

    description = models.TextField(
        blank=True,
        help_text="Public description of the provider",
    )

    mechanism_type = models.CharField(
        max_length=10,
        choices=SpfMechanism,
        help_text="Type of SPF mechanism used",
    )

    mechanism_value = models.CharField(
        max_length=255,
        help_text="The actual SPF mechanism value (e.g., 'include:_spf.google.com')",
    )

    lookup_count = models.PositiveSmallIntegerField(
        default=1,
        help_text="Number of DNS lookups this mechanism requires",
    )

    priority = models.PositiveSmallIntegerField(
        default=100,
        help_text="Order in which this should appear in combined SPF record",
    )

    active = models.BooleanField(
        default=True,
        help_text="Whether this provider is currently available for selection",
    )

    notes = models.TextField(
        blank=True,
        help_text="Internal notes about this provider",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the EmailProvider model."""

        ordering: ClassVar = ["priority", "name"]

    def __str__(self) -> str:
        """Returns the name of the provider when converted to a string."""
        # pyrefly: ignore [bad-return]
        return self.name

    def get_mechanism(self) -> str:
        """Returns the complete SPF mechanism string for this provider.

        Returns:
            str: Formatted SPF mechanism string
        """
        return f"{self.mechanism_type}:{self.mechanism_value}"

    @staticmethod
    def validate_combination(providers: list[EmailProvider]) -> tuple[bool, str | None]:
        """Validates whether a combination of providers can be used together.

        Args:
            providers: List of EmailProvider instances to validate

        Returns:
            Tuple containing:
                - Boolean indicating if combination is valid
                - Error message if invalid, None if valid
        """
        # Check total lookup count
        total_lookups = sum(p.lookup_count for p in providers)
        max_lookups = 10
        if total_lookups > max_lookups:
            return False, f"Total DNS lookups ({total_lookups}) exceeds maximum of 10"

        # Calculate total mechanism length (including basic SPF framework)
        mechanisms = " ".join(p.get_mechanism() for p in providers)
        spf_record = f"v=spf1 {mechanisms} -all"
        max_spf_length = 255
        if len(spf_record) > max_spf_length:
            return False, "Combined SPF record exceeds 255 characters"

        return True, None
