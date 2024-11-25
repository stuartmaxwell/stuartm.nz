"""Views for the contact_form app."""

import asyncio

from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from contact_form.forms import ContactForm
from contact_form.tasks import send_email_async

background_tasks = set()


# A simple view to display the converter HTML template.
async def contact_form(request: HttpRequest, contact_form_title: str = "Contact Form") -> HttpResponse:
    """Async view for the contact form.

    This displays the contact form, or processes the form data if it was submitted and then displays the success.

    An optional title can be passed in to customise the title of the contact form. This is useful so the form can be
    used in multiple places with different titles. For example, in the spf_generator app, the contact form is added to
    `urls.py` file as follows:

    ```python
    urlpatterns = [
        path("contact/", contact_form, {"contact_form_title": "Request a New SPF Record"}, name="contact_form"),
        path("", generate_spf_record, name="spf_generator"),
        ]
    ```

    Args:
        request (HttpRequest): The HTTP request.
        contact_form_title (str): The title for the contact form.

    Returns:
        HttpResponse: The HTTP response.
    """
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
