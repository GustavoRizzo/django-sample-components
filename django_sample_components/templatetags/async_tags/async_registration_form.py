from django.template.loader import render_to_string
from django.utils.safestring import SafeString

from django_sample_components.forms.registration_form import RegistrationForm


def async_registration_form(context) -> SafeString:
    """
    Renders a self-contained registration form with inline per-field HTMX validation.

    Username uniqueness is checked on keyup (after >3 chars). Subject enrollment capacity
    is checked on change. On valid submit, a success message replaces the form. On invalid
    submit, the form re-renders with crispy-forms error display.

    Usage:
        {% load async_tags %}
        {% async_registration_form %}
    """
    return render_to_string(
        "django_sample_components/components/async_registration_form.html",
        {"form": RegistrationForm()},
        request=context.get("request"),
    )
