"""Forms for the contact_form app."""

from django import forms


class ContactForm(forms.Form):
    """Form for the contact form."""

    name = forms.CharField(
        label="Your name",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name",
                "class": "form-control",
            },
        ),
    )

    email = forms.EmailField(
        label="Your email",
        max_length=100,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email",
                "class": "form-control",
            },
        ),
    )

    message = forms.CharField(
        label="Your message",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Your message",
                "class": "form-control",
            },
        ),
    )

    honeypot = forms.CharField(
        label="Leave empty",
        required=False,
        widget=forms.HiddenInput,
    )
