import uuid

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import SafeString


def async_active_search(
    context,
    search_url: str | None = None,
    placeholder: str = "Begin typing to search...",
    min_chars: int = 1,
) -> SafeString:
    """
    Renders an active-search component that filters results on every keystroke using HTMX.

    Sends a GET request to the server on each input change (debounced 300ms) and replaces
    the results table inline without a page reload.

    Args:
        search_url:  URL that handles search GET requests. Defaults to the built-in demo endpoint.
        placeholder: Input placeholder text.
        min_chars:   Minimum characters required before the first search triggers.

    Example:
        {% load async_tags %}
        {% async_active_search %}
        {% async_active_search placeholder="Search contacts..." min_chars=2 %}
        {% async_active_search search_url="/my-app/search/" %}
    """
    request = context.get("request")
    id_active_search = f"async-active-search-{uuid.uuid4()}"

    component_context = {
        "id_active_search": id_active_search,
        "search_url": search_url or reverse("django_sample_components:active_search_component"),
        "placeholder": placeholder,
        "min_chars": min_chars,
    }

    return render_to_string(
        "django_sample_components/components/async_active_search.html",
        component_context,
        request=request,
    )
