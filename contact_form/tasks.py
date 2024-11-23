"""Contact Form Tasks."""

import time

import httpx
from django.conf import settings
from django_tasks import task


@task()
def send_email(message: str, name: str = "", email: str = "") -> None:
    """Send an email with django-tasks using Resend's API."""
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": settings.CONTACT_FORM_FROM,
        "to": settings.CONTACT_FORM_TO,
        "subject": "Contact Form Submission from stuartm.nz",
        "html": f"<ul><li>Name: {name}</li><li>Email: {email}</li><li>Message:<br>{message}</li></ul>",
        "text": f"Name: {name}\n\nEmail: {email}\n\nMessage:\n\n{message}\n\n",
    }

    # sleep for 5 seconds to simulate a slow API call
    time.sleep(5)

    httpx.post(url, headers=headers, json=payload)


@task()
async def send_email_async(message: str, name: str = "", email: str = "") -> None:
    """Asynchronously send an email using Resend's API."""
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": settings.CONTACT_FORM_FROM,
        "to": settings.CONTACT_FORM_TO,
        "subject": "Contact Form Submission from stuartm.nz",
        "html": f"<ul><li>Name: {name}</li><li>Email: {email}</li><li>Message:<br>{message}</li></ul>",
        "text": f"Name: {name}\n\nEmail: {email}\n\nMessage:\n\n{message}\n\n",
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)
