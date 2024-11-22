"""Views for the contact_form app."""

import asyncio

from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from contact_form.forms import ContactForm
from contact_form.tasks import send_email_async

background_tasks = set()


# A simple view to display the converter HTML template.
async def contact_form(request: HttpRequest, contact_form_title: str = "Contact Form") -> HttpResponse:
    """Render the contact form template."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Send the email - see RUFF006
            task = asyncio.create_task(send_email_async(name=name, email=email, message=message))
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)

            # Show a success message
            return TemplateResponse(request, "contact_form/success.html")
    else:
        form = ContactForm()

    return TemplateResponse(
        request,
        "contact_form/contact_form.html",
        {"form": form, "contact_form_title": contact_form_title},
    )
