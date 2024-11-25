"""Contact Form Tasks."""

import httpx
from django.conf import settings


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
        "reply_to": email,
        "subject": "Contact Form Submission from stuartm.nz",
        "html": f"<ul><li>Name: {name}</li><li>Email: {email}</li><li>Message:<br>{message}</li></ul>",
        "text": f"Name: {name}\n\nEmail: {email}\n\nMessage:\n\n{message}\n\n",
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)
