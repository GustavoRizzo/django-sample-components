from django.template.loader import render_to_string
from django.utils.safestring import SafeString

from django_sample_components.forms.sum_form import SumForm


def async_sum_form(context) -> SafeString:
    """
    Renders a self-contained sum form powered by HTMX and django-crispy-forms.

    The form submits two numbers and displays their sum inline, without a full page reload.
    HTMX POSTs to the dynamic_forms_sum_component endpoint and replaces the component via outerHTML swap.

    Usage:
        {% load async_tags %}
        {% async_sum_form %}
    """
    return render_to_string(
        "django_sample_components/components/async_sum_form.html",
        {"form": SumForm(), "result": None},
        request=context.get("request"),
    )
