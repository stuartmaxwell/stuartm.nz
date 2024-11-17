"""Views for the SPF Generator app."""

from typing import Any

from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from spf_generator.models import EmailProvider, ProviderCategory, SpfAllMechanism


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
                    help_text=provider.description,
                )


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
                    provider = EmailProvider.objects.get(id=provider_id)
                    selected_providers.append(provider)

            # Check if any providers were selected
            if not selected_providers:
                response = render(
                    request,
                    "spf_generator/partials/error.html",
                    {"error": "Please select at least one email provider"},
                )
                response["HX-Retarget"] = "#result"
                return response

            # Check total lookup count
            total_lookups = sum(p.lookup_count for p in selected_providers)
            max_dns_lookups = 10
            if total_lookups > max_dns_lookups:
                response = render(
                    request,
                    "spf_generator/partials/error.html",
                    {"error": f"Total DNS lookups ({total_lookups}) exceeds maximum of 10"},
                )
                response["HX-Retarget"] = "#result"
                return response

            # Generate SPF record with selected 'all' mechanism
            mechanisms = " ".join(
                p.get_mechanism()
                for p in sorted(
                    selected_providers,
                    key=lambda x: x.priority,
                )
            )
            all_mechanism = SpfAllMechanism(form.cleaned_data["all_mechanism"])
            spf_record = f"v=spf1 {mechanisms} {all_mechanism}"

            # Check record length
            max_record_length = 255
            if len(spf_record) > max_record_length:
                return render(
                    request,
                    "spf_generator/partials/error.html",
                    {"error": "Combined SPF record exceeds 255 characters"},
                    headers={"HX-Retarget": "#result"},
                )

            # Success - render SPF record
            response = render(
                request,
                "spf_generator/partials/result.html",
                {
                    "spf_record": spf_record,
                    "all_mechanism": all_mechanism.label,
                    "all_mechanism_description": all_mechanism.description,
                },
            )
            response["HX-Retarget"] = "#result"
            return response

        # Form validation failed
        response = render(
            request,
            "spf_generator/partials/error.html",
            {"error": "Invalid form submission"},
        )
        response["HX-Retarget"] = "#result"
        return response

    # GET request - display form
    providers = {provider.id: provider for provider in EmailProvider.objects.filter(active=True)}

    context = {
        "form": ProviderSelectForm(),
        "categories": ProviderCategory.choices,
        "providers": providers,  # Add this line
    }
    return render(request, "spf_generator/generator.html", context)
