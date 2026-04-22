from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe

from django_sample_components.templatetags.async_tags.async_lazy_popup import async_lazy_popup

_SPINNER = mark_safe(
    '<div class="d-flex align-items-center gap-2 text-muted">'
    '<div class="spinner-border spinner-border-sm" role="status" aria-label="Loading"></div>'
    "<span>Loading...</span>"
    "</div>"
)


def async_popup_registration_form(
    context,
    name_button: str = "Open Registration",
    title: str = "Registration Form",
    size: str | None = None,
) -> SafeString:
    """
    Renders a Bootstrap 5 modal button that lazy-loads the registration form when opened.

    The form is re-fetched from the server every time the modal opens (always_reload_on_open=True),
    so the user always starts with a fresh, empty form.

    Args:
        name_button:    Label of the button that triggers the modal. Default: "Open Registration".
        title:          Title displayed in the modal header. Default: "Registration Form".
        size:           Bootstrap modal size modifier: "sm", "lg", or "xl". Omitted if not set.

    Example:
        {% load async_tags %}
        {% async_popup_registration_form %}
        {% async_popup_registration_form name_button="Register" title="Sign Up" size="lg" %}
    """
    content_url = reverse("django_sample_components:popup_registration_form_component")

    return async_lazy_popup(
        context,
        content=_SPINNER,
        name_button=name_button,
        title=title,
        content_url=content_url,
        size=size,
        always_reload_on_open=True,
    )
