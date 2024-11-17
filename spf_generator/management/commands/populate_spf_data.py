"""Management command to populate the SPF data."""

from typing import Any

from django.core.management.base import BaseCommand

from spf_generator.models import EmailProvider, ProviderCategory, SpfMechanism


class Command(BaseCommand):
    """Management command to populate the database with common email provider SPF records.

    Save this file as your_app_name/management/commands/populate_spf_providers.py
    """

    help = "Populates the database with common email provider SPF records"

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ANN401, ARG002
        """Handle the command execution."""
        # Email Hosting Providers
        email_hosting_providers = [
            {
                "name": "Google Workspace",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Google Workspace (formerly G Suite) email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "_spf.google.com",
                "lookup_count": 2,
                "priority": 10,
                "notes": "Includes gmail.com and googlemail.com domains",
            },
            {
                "name": "Microsoft 365",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Microsoft 365 (formerly Office 365) email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.protection.outlook.com",
                "lookup_count": 2,
                "priority": 10,
                "notes": "Used for all Microsoft 365 email services",
            },
            {
                "name": "Zoho Mail",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Zoho Mail hosting service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "zoho.com",
                "lookup_count": 1,
                "priority": 10,
                "notes": "Basic Zoho Mail SPF record",
            },
            {
                "name": "FastMail",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "FastMail email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.messagingengine.com",
                "lookup_count": 1,
                "priority": 10,
                "notes": "Covers all FastMail sending IPs",
            },
            {
                "name": "ProtonMail",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "ProtonMail secure email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.protonmail.ch",
                "lookup_count": 1,
                "priority": 10,
                "notes": "Covers all ProtonMail infrastructure",
            },
        ]

        # Transactional Email Providers
        transactional_providers = [
            {
                "name": "Amazon SES",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Amazon Simple Email Service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "amazonses.com",
                "lookup_count": 1,
                "priority": 20,
                "notes": "Note: Region-specific SPF records are also available",
            },
            {
                "name": "SendGrid",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "SendGrid email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "sendgrid.net",
                "lookup_count": 1,
                "priority": 20,
                "notes": "Covers all SendGrid sending IPs",
            },
            {
                "name": "Mailgun",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Mailgun email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "mailgun.org",
                "lookup_count": 1,
                "priority": 20,
                "notes": "Basic Mailgun SPF record",
            },
            {
                "name": "Postmark",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Postmark email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.mtasv.net",
                "lookup_count": 1,
                "priority": 20,
                "notes": "Covers all Postmark sending servers",
            },
            {
                "name": "Mailchimp",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Mailchimp Transactional (formerly Mandrill)",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.mandrillapp.com",
                "lookup_count": 1,
                "priority": 20,
                "notes": "Used for Mailchimp Transactional emails",
            },
        ]

        # Other Common Services
        other_providers = [
            {
                "name": "Outlook.com",
                "category": ProviderCategory.OTHER,
                "description": "Personal Outlook.com/Hotmail accounts",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.protection.outlook.com",
                "lookup_count": 2,
                "priority": 30,
                "notes": "For personal Microsoft email accounts (not Microsoft 365)",
            },
            {
                "name": "Yahoo Mail",
                "category": ProviderCategory.OTHER,
                "description": "Yahoo Mail service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.mail.yahoo.com",
                "lookup_count": 1,
                "priority": 30,
                "notes": "Covers Yahoo Mail infrastructure",
            },
        ]

        # Combine all providers
        all_providers = email_hosting_providers + transactional_providers + other_providers

        # Create providers in database
        for provider_data in all_providers:
            EmailProvider.objects.get_or_create(
                name=provider_data["name"],
                defaults=provider_data,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created provider: {provider_data["name"]}'),
            )
