"""Views for the SPF Generator app."""

from typing import TYPE_CHECKING

from django.shortcuts import render

from spf_generator.forms import ProviderSelectForm
from spf_generator.models import EmailProvider, ProviderCategory, SpfAllMechanism

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def generate_spf_record(request: HttpRequest) -> HttpResponse:
    """View function for the SPF record generator.

    Displays the provider selection form on GET requests.
    Processes form submission and generates SPF record on POST requests.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponse containing either the full page or HTMX partial
    """
    if request.method == "POST":
        form = ProviderSelectForm(request.POST)
        if form.is_valid():
            # Get selected providers
            selected_providers: list[EmailProvider] = []
            for field_name, value in form.cleaned_data.items():
                if value and field_name.startswith("provider_"):
                    provider_id = int(field_name.split("_")[1])
                    # pyrefly: ignore [missing-attribute]
                    provider = EmailProvider.objects.get(id=provider_id)
                    selected_providers.append(provider)

            # Check if either providers are selected or custom IP is provided
            custom_ip = form.cleaned_data.get("custom_ip", "")
            if not selected_providers and not custom_ip:
                return render(
                    request,
                    "spf_generator/partials/error.html",
                    {"error": "Please select at least one email provider or enter a custom IP address"},
                )
            # Check total lookup count
            total_lookups = sum(p.lookup_count for p in selected_providers)
            max_dns_lookups = 10
            if total_lookups > max_dns_lookups:
                return render(
                    request,
                    "spf_generator/partials/error.html",
                    {"error": f"Total DNS lookups ({total_lookups}) exceeds maximum of 10"},
                )

            # Generate SPF record
            mechanisms = []

            # Add custom IP first if provided
            if custom_ip:
                mechanisms.append(custom_ip)

            # Add provider mechanisms
            mechanisms.extend(
                p.get_mechanism()
                for p in sorted(
                    selected_providers,
                    key=lambda x: x.priority,
                )
            )

            spf_record = f"v=spf1 {' '.join(mechanisms)} {form.cleaned_data['all_mechanism']}"

            # Check record length
            max_record_length = 255
            if len(spf_record) > max_record_length:
                return render(
                    request,
                    "spf_generator/partials/error.html",
                    {"error": "Combined SPF record exceeds 255 characters"},
                )

            all_mechanism = SpfAllMechanism(form.cleaned_data["all_mechanism"])

            # Success - render SPF record
            return render(
                request,
                "spf_generator/partials/result.html",
                {
                    "spf_record": spf_record,
                    "all_mechanism": all_mechanism.label,
                    "all_mechanism_description": all_mechanism.description,
                },
            )

        # Form validation failed - must be the IP address if this point is reached
        return render(
            request,
            "spf_generator/partials/error.html",
            {"error": "Invalid form submission - please check if you've entered an invalid IP address"},
        )

    # GET request - display form
    # pyrefly: ignore [missing-attribute]
    providers = {provider.pk: provider for provider in EmailProvider.objects.filter(active=True)}

    context = {
        "form": ProviderSelectForm(),
        "categories": ProviderCategory.choices,
        "providers": providers,  # Add this line
    }
    return render(request, "spf_generator/generator.html", context)
