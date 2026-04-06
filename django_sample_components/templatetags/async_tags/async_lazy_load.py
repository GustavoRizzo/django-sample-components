import uuid

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import SafeString


def async_lazy_load(
    context,
    url: str | None = None,
    placeholder: str = "Scroll down to load content from the server.",
    delay_ms: int | None = None,
) -> SafeString:
    """
    Renders an HTMX lazy-load component that fetches content on reveal.

    The component performs a GET request only once, when it enters the viewport.

    Args:
        url: Target URL to be fetched by HTMX. Can be internal or external.
        placeholder: Initial text shown before the lazy content is loaded.
        delay_ms: Optional server delay in milliseconds before returning content.

    Example:
        {% load async_tags %}
        {% async_lazy_load %}
        {% async_lazy_load url="/async/lazy-load/" %}
        {% async_lazy_load placeholder="Custom loading message" %}
        {% async_lazy_load delay_ms=1200 %}
    """
    request = context.get("request")

    component_context = {
        "id_lazy_load": f"async-lazy-load-{uuid.uuid4()}",
        "url": url or reverse("django_sample_components:lazy_load"),
        "placeholder": placeholder,
        "delay_ms": delay_ms,
    }

    return render_to_string(
        "django_sample_components/components/async_lazy_load.html",
        component_context,
        request=request,
    )
