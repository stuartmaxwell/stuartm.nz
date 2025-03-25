"""Forms for the spf_generator app."""

import ipaddress
from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from spf_generator.models import EmailProvider, ProviderCategory, SpfAllMechanism


def validate_ip_address(value: str) -> None:
    """Validates if the string is a valid IPv4 or IPv6 address.

    Args:
        value: String to validate

    Raises:
        ValidationError: If the string is not a valid IP address
    """
    if not value:
        return

    try:
        ipaddress.ip_address(value)
    except ValueError as exc:
        msg = "Please enter a valid IP address"
        raise ValidationError(msg) from exc


class ProviderSelectForm(forms.Form):
    """Form for selecting email providers.

    The form dynamically generates checkboxes for each active provider,
    grouped by category.
    """

    all_mechanism = forms.ChoiceField(
        choices=SpfAllMechanism.choices,
        initial=SpfAllMechanism.FAIL,
        required=True,
        help_text=(
            "<p>Choose how to handle mail from unlisted servers:</p>"
            "<ul>"
            "<li><strong>Fail (-all)</strong>: Recommended. Explicitly reject mail from unlisted servers. "
            "Use this if you're sure you've listed all legitimate sending servers.</li>"
            "<li><strong>Softfail (~all)</strong>: Suggest rejection but don't enforce it. "
            "Useful during SPF testing or if you're unsure about all legitimate senders.</li>"
            "<li><strong>Neutral (?all)</strong>: Take no position on unlisted servers. "
            "Not recommended as it doesn't help prevent email spoofing.</li>"
            "</ul>"
        ),
        widget=forms.Select(
            attrs={
                "aria-label": "SPF All Mechanism",
                "class": "form-select",
            },
        ),
    )

    custom_ip = forms.CharField(
        required=False,
        validators=[validate_ip_address],
        help_text="If you have a server that sends email, enter its IP address here",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g., 192.168.1.1 or 2001:db8::1",
                "aria-label": "Custom IP Address",
            },
        ),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Initializes the form with provider fields."""
        super().__init__(*args, **kwargs)

        # Group providers by category
        for category in ProviderCategory.choices:
            providers = EmailProvider.objects.filter(
                category=category[0],
                active=True,
            )

            for provider in providers:
                field_name = f"provider_{provider.id}"
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=provider.name,
                    help_text=provider.mechanism_value,
                )

    def clean_custom_ip(self) -> str:
        """Clean and validate the custom IP address.

        Returns:
            str: The cleaned IP address or empty string
        """
        ip = self.cleaned_data.get("custom_ip", "").strip()
        if ip:
            try:
                # Determine if IPv4 or IPv6 and format accordingly
                ip_obj = ipaddress.ip_address(ip)
            except ValueError as exc:
                msg = "Please enter a valid IP address"
                raise ValidationError(msg) from exc
            else:
                if isinstance(ip_obj, ipaddress.IPv6Address):
                    return f"ip6:{ip}"
                return f"ip4:{ip}"
        return ""
