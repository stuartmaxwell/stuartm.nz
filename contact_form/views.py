"""Views for the contact_form app."""

from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from contact_form.forms import ContactForm
from contact_form.tasks import send_email

background_tasks = set()


# A simple view to display the converter HTML template.
def contact_form(request: HttpRequest, contact_form_title: str = "Contact Form") -> HttpResponse:
    """Render the contact form template."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_email.enqueue(name=name, email=email, message=message)

            # Show a success message
            return TemplateResponse(request, "contact_form/success.html")
    else:
        form = ContactForm()

    return TemplateResponse(
        request,
        "contact_form/contact_form.html",
        {"form": form, "contact_form_title": contact_form_title},
    )
