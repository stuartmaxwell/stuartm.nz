"""Context processors for the project."""


def debug_processor(_) -> dict:  # noqa: ANN001
    """Add the DEBUG setting to the context."""
    from django.conf import settings  # noqa: PLC0415

    return {"DEBUG": settings.DEBUG}
