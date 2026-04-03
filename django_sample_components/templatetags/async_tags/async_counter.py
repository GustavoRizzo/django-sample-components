import uuid

from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def async_counter(
    context,
    initial_value: int = 0,
    step: int = 1,
    min_value: int | None = None,
    max_value: int | None = None,
) -> SafeString:
    """
    Renders an interactive counter component with +/− buttons using HTMX.

    When buttons are clicked, HTMX sends a POST request to update the value
    without reloading the page.

    Args:
        initial_value: Starting value of the counter. Default: 0.
        step:          Increment/decrement amount. Default: 1.
        min_value:     Minimum allowed value (optional). Can be used for frontend validation.
        max_value:     Maximum allowed value (optional). Can be used for frontend validation.

    Example:
        {% load async_tags %}
        {% async_counter initial_value=0 step=1 %}
        {% async_counter initial_value=5 step=1 min_value=0 max_value=10 %}
    """
    request = context.get("request")
    id_counter = f"async-counter-{uuid.uuid4()}"

    component_context = {
        "id_counter": id_counter,
        "initial_value": initial_value,
        "step": step,
        "min_value": min_value,
        "max_value": max_value,
    }

    return render_to_string(
        "django_sample_components/components/async_counter.html",
        component_context,
        request=request,
    )
