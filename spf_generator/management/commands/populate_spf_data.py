"""Management command to populate the SPF data."""

from typing import Any

from django.core.management.base import BaseCommand

from spf_generator.models import EmailProvider, ProviderCategory, SpfMechanism


class Command(BaseCommand):
    """Management command to populate the database with common email provider SPF records.

    Save this file as your_app_name/management/commands/populate_spf_providers.py
    """

    help = "Populates the database with common email provider SPF records"

    # pyrefly: ignore [bad-override]
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
                "notes": (
                    "Includes gmail.com and googlemail.com domains\n"
                    "https://support.google.com/a/answer/33786?sjid=13899028837607159847-AP#spf-value"
                ),
            },
            {
                "name": "Microsoft 365",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Microsoft 365 (formerly Office 365) email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.protection.outlook.com",
                "lookup_count": 2,
                "priority": 10,
                "notes": (
                    "Used for all Microsoft 365 email services.\n"
                    "https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure"
                ),
            },
            {
                "name": "FastMail",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "FastMail email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.messagingengine.com",
                "lookup_count": 1,
                "priority": 10,
                "notes": (
                    "Covers all FastMail sending IPs.\n"
                    "https://www.fastmail.help/hc/en-us/articles/360060591153-Manual-DNS-configuration"
                ),
            },
            {
                "name": "ProtonMail",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "ProtonMail secure email hosting",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "_spf.protonmail.ch",
                "lookup_count": 1,
                "priority": 10,
                "notes": (
                    "Covers all ProtonMail infrastructure\nhttps://proton.me/support/anti-spoofing-custom-domain"
                ),
            },
            {
                "name": "Zoho Mail India",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Zoho Mail India hosting service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "zoho.in",
                "lookup_count": 1,
                "priority": 10,
                "notes": "India-specific Zoho Mail SPF record",
            },
            {
                "name": "Zoho Mail Europe",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Zoho Mail Europe hosting service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.zoho.eu",
                "lookup_count": 1,
                "priority": 10,
                "notes": "Europe Zoho Mail SPF record",
            },
            {
                "name": "Zoho Mail Global",
                "category": ProviderCategory.EMAIL_HOSTING,
                "description": "Zoho Mail global hosting service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "zoho.com",
                "lookup_count": 1,
                "priority": 10,
                "notes": "Global Zoho Mail SPF record",
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
                "notes": (
                    "Note: Region-specific SPF records are also available\n"
                    "https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-spf.html"
                ),
            },
            {
                "name": "SendGrid",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "SendGrid email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "sendgrid.net",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Covers all SendGrid sending IPs\n"
                    "https://www.twilio.com/docs/sendgrid/ui/account-and-settings/spf-records"
                ),
            },
            {
                "name": "Mailgun",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Mailgun email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "mailgun.org",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Basic Mailgun SPF record.\n"
                    "https://help.mailgun.com/hc/en-us/articles/360026833053-Domain-Verification-Setup-Guide"
                ),
            },
            {
                "name": "Postmark",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Postmark email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.mtasv.net",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Covers all Postmark sending servers\n"
                    "https://postmarkapp.com/guides/spf#2-create-your-spf-record"
                ),
            },
            {
                "name": "SparkPost Global",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "SparkPost email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "_spf.sparkpostmail.com",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Covers global SparkPost sending servers. Europe have different settings\n"
                    "https://support.sparkpost.com/docs/faq/sender-id-spf-failures"
                ),
            },
            {
                "name": "SparkPost Europe",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "SparkPost Europe email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "_spf.eu.sparkpostmail.com",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Covers Europe SparkPost sending servers. Global have different settings\n"
                    "https://support.sparkpost.com/docs/faq/sender-id-spf-failures"
                ),
            },
            {
                "name": "MailJet",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "MailJet email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "spf.mailjet.com",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Covers all MailJet sending servers\n"
                    "https://documentation.mailjet.com/hc/en-us/articles/360042412734-Authenticating-Domains-with-SPF-DKIM"
                ),
            },
            {
                "name": "Scaleway",
                "category": ProviderCategory.TRANSACTIONAL,
                "description": "Scaleway email delivery service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "_spf.tem.scaleway.com",
                "lookup_count": 1,
                "priority": 20,
                "notes": (
                    "Covers all Scaleway sending servers\n"
                    "https://www.scaleway.com/en/docs/managed-services/transactional-email/how-to/add-spf-dkim-records-to-your-domain/"
                ),
            },
        ]

        # Other Common Services
        other_providers = [
            {
                "name": "Zendesk",
                "category": ProviderCategory.OTHER,
                "description": "Zendesk helpdesk service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "mail.zendesk.com",
                "lookup_count": 40,
                "priority": 30,
                "notes": (
                    "For Zendesk customers.\n"
                    "https://support.zendesk.com/hc/en-us/articles/4408832543770-Allowing-Zendesk-to-send-email-on-behalf-of-your-email-domain"
                ),
            },
            {
                "name": "Freshdesk",
                "category": ProviderCategory.OTHER,
                "description": "Freshdesk helpdesk service",
                "mechanism_type": SpfMechanism.INCLUDE,
                "mechanism_value": "email.freshdesk.com",
                "lookup_count": 40,
                "priority": 30,
                "notes": (
                    "For Freshdesk customers.\n"
                    "https://support.freshdesk.com/support/solutions/articles/43170-creating-an-spf-record-to-ensure-proper-email-delivery"
                ),
            },
        ]

        # Combine all providers
        all_providers = email_hosting_providers + transactional_providers + other_providers

        # Create providers in database
        for provider_data in all_providers:
            # pyrefly: ignore [missing-attribute]
            EmailProvider.objects.get_or_create(
                name=provider_data["name"],
                defaults=provider_data,
            )
            self.stdout.write(
                # pyrefly: ignore [missing-attribute]
                self.style.SUCCESS(f'Created provider: {provider_data["name"]}'),
            )
