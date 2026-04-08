import uuid

from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def async_htmx_loader(
    context,
    url_htmx: str,
    id_target: str | None = None,
    hx_trigger: str = "load",
    hx_on_after_swap: str | None = None,
    text_preload: str = "Loading, please wait...",
) -> SafeString:
    """
    Renders a generic HTMX GET loader with a Bootstrap spinner.

    Fires a GET request to `url_htmx` on the given `hx_trigger` and replaces
    the inner div (identified by `id_target`) with the server response.

    Args:
        url_htmx: URL to fetch via HTMX GET.
        id_target: ID for the target div. Auto-generated if not provided.
        hx_trigger: HTMX trigger expression (default: "load").
        hx_on_after_swap: Optional JS expression for hx-on::after-swap.
        text_preload: Text shown alongside the spinner while loading.

    Example:
        {% load async_tags %}
        {% async_htmx_loader url_htmx="/async/counter/component/?initial_value=0" %}
        {% async_htmx_loader url_htmx="/api/data/" hx_trigger="revealed once" %}
    """
    request = context.get("request")
    resolved_id = id_target or f"htmx-loader-{uuid.uuid4()}"

    component_context = {
        "url_htmx": url_htmx,
        "id_target": resolved_id,
        "hx_trigger": hx_trigger,
        "hx_on_after_swap": hx_on_after_swap,
        "text_preload": text_preload,
    }

    return render_to_string(
        "django_sample_components/components/async_htmx_loader.html",
        component_context,
        request=request,
    )
