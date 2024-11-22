"""Views for the contact_form app."""

from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from contact_form.forms import ContactForm


# A simple view to display the converter HTML template.
def contact_form(request: HttpRequest) -> HttpResponse:
    """Render the contact form template."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            # Send the email
            send_mail(
                subject=f"Contact form submission from {name}",
                message=message,
                from_email=email,
                recipient_list=["stuart@amanzi.nz"],
                fail_silently=False,
            )
            # Show a success message
            return render(request, "contact_form/success.html")
    else:
        form = ContactForm()
    return render(request, "contact_form/contact_form.html", {"form": form})
