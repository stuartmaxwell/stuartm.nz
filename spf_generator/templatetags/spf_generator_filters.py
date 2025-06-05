"""Custom template filters for spf_generator app."""
# your_app_name/templatetags/spf_generator_filters.py

from django import template
from django.template.defaultfilters import stringfilter

from spf_generator.models import EmailProvider

register = template.Library()


@register.filter
@stringfilter
def startswith(text: str, starts: str) -> bool:
    """Template filter to check if a string starts with given text.

    Args:
        text: String to check
        starts: Prefix to look for

    Returns:
        bool: True if text starts with given prefix
    """
    return text.startswith(starts)


@register.filter
def get_provider(providers_dict: dict[int, EmailProvider], field_name: str) -> EmailProvider:
    """Template filter to get provider object from field name.

    Args:
        providers_dict: Dictionary of providers
        field_name: Form field name (e.g., 'provider_1')

    Returns:
        EmailProvider: The provider object or None
    """
    provider_id = int(field_name.split("_")[1])

    provider = providers_dict.get(provider_id)
    if not provider:
        msg = f"Provider with ID {provider_id} not found."
        raise ValueError(msg)

    return provider
