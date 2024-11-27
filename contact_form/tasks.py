"""Contact Form Tasks."""

import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

SUCESS_STATUS_CODE = 200


async def send_email_async(message: str, name: str = "", email: str = "") -> None:
    """Asynchronously send an email using Resend's API.

    Args:
        message (str): The message to send.
        name (str): The name of the sender.
        email (str): The email of the sender.

    Returns:
        None: The function does not return anything.
    """
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
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code != SUCESS_STATUS_CODE:
            logger.error(f"Failed to send email: {response.status_code}. Payload: {payload}")
        else:
            logger.debug(f"Email sent successfully: {response.status_code}. Payload: {payload}")
