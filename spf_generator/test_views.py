"""Basic tests for the views.py file."""

import pytest
from django.test import Client, RequestFactory
from django.urls import reverse
from spf_generator.models import EmailProvider, ProviderCategory, SpfMechanism
from spf_generator.views import generate_spf_record


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def email_providers():
    """Create some test email providers."""
    providers = [
        EmailProvider.objects.create(
            name="Google Workspace",
            category=ProviderCategory.EMAIL_HOSTING,
            mechanism_type=SpfMechanism.INCLUDE,
            mechanism_value="_spf.google.com",
            lookup_count=2,
            priority=10,
        ),
        EmailProvider.objects.create(
            name="SendGrid",
            category=ProviderCategory.TRANSACTIONAL,
            mechanism_type=SpfMechanism.INCLUDE,
            mechanism_value="sendgrid.net",
            lookup_count=1,
            priority=20,
        ),
        EmailProvider.objects.create(
            name="Office 365",
            category=ProviderCategory.EMAIL_HOSTING,
            mechanism_type=SpfMechanism.INCLUDE,
            mechanism_value="spf.protection.outlook.com",
            lookup_count=2,
            priority=10,
        ),
    ]
    return providers


@pytest.mark.django_db
class TestSpfGenerator:
    def test_get_form(self, client):
        """Test that the form loads correctly."""
        url = reverse("spf_generator:spf_generator")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_without_providers(self, client):
        """Test submission without selecting any providers."""
        url = reverse("spf_generator:spf_generator")
        response = client.post(url, {"all_mechanism": "-all"})
        assert b"Please select at least one email provider" in response.content

    def test_post_with_single_provider(self, client, email_providers):
        """Test generating SPF record with a single provider."""
        url = reverse("spf_generator:spf_generator")
        data = {"all_mechanism": "-all", f"provider_{email_providers[0].id}": True}
        response = client.post(url, data)
        assert response.status_code == 200
        assert b"include:_spf.google.com -all" in response.content

    def test_post_with_multiple_providers(self, client, email_providers):
        """Test generating SPF record with multiple providers."""
        url = reverse("spf_generator:spf_generator")
        data = {
            "all_mechanism": "-all",
            f"provider_{email_providers[0].id}": True,
            f"provider_{email_providers[1].id}": True,
        }
        response = client.post(url, data)
        assert response.status_code == 200
        # Check that both providers are in the SPF record
        assert b"include:_spf.google.com" in response.content
        assert b"include:sendgrid.net" in response.content

    def test_lookup_count_limit(self, client, email_providers):
        """Test that the 10 lookup limit is enforced."""
        # Create a provider with 9 lookups
        high_lookup_provider = EmailProvider.objects.create(
            name="High Lookup Provider",
            category=ProviderCategory.OTHER,
            mechanism_type=SpfMechanism.INCLUDE,
            mechanism_value="test.com",
            lookup_count=9,
            priority=30,
        )

        url = reverse("spf_generator:spf_generator")
        data = {
            "all_mechanism": "-all",
            f"provider_{email_providers[0].id}": True,  # 2 lookups
            f"provider_{high_lookup_provider.pk}": True,  # 9 lookups
        }
        response = client.post(url, data)
        assert b"exceeds maximum of 10" in response.content

    @pytest.mark.parametrize(
        "mechanism,expected",
        [
            ("-all", b"-all"),
            ("~all", b"~all"),
            ("?all", b"?all"),
        ],
    )
    def test_all_mechanism_options(self, client, email_providers, mechanism, expected):
        """Test different 'all' mechanism options."""
        url = reverse("spf_generator:spf_generator")
        data = {
            "all_mechanism": mechanism,
            f"provider_{email_providers[0].id}": True,
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert expected in response.content

    def test_provider_ordering(self, client, email_providers):
        """Test that providers are ordered by priority."""
        url = reverse("spf_generator:spf_generator")
        data = {
            "all_mechanism": "-all",
            f"provider_{email_providers[0].id}": True,  # Email hosting (priority 10)
            f"provider_{email_providers[1].id}": True,  # Transactional (priority 20)
        }
        response = client.post(url, data)
        content = response.content.decode()
        # Check that Google Workspace (priority 10) comes before SendGrid (priority 20)
        assert content.index("_spf.google.com") < content.index("sendgrid.net")
