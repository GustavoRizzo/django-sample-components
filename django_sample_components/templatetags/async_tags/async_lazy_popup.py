from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import SafeString

from django_sample_components.templatetags.sample_tags.simple_popup import _build_modal_base_context


def async_lazy_popup(
    context,
    name_button: str = "Open",
    title: str = "Popup Title",
    content_url: str | None = None,
    size: str | None = None,
    always_reload_on_open: bool = False,
) -> SafeString:
    """
    Renders a Bootstrap 5 modal that lazy-loads its body content via HTMX when opened.

    The modal opens instantly with a loading spinner. The GET request to fetch the real
    content is triggered by the Bootstrap 'show.bs.modal' event, so the server is only
    called when the user actually opens the popup.

    Args:
        name_button:    Label of the button that triggers the modal. Default: "Open".
        title:          Title displayed in the modal header. Default: "Popup Title".
        content_url:    URL to fetch the modal body content from. Defaults to the built-in demo endpoint.
        size:           Bootstrap modal size modifier: "sm", "lg", or "xl". Omitted if not set.
        always_reload_on_open: When True, content is re-fetched every time the modal opens. When False
                        (default), content is fetched only on the first open — the HTMX trigger
                        element is removed from the DOM after the first load (outerHTML swap).

    Example:
        {% load async_tags %}
        {% async_lazy_popup name_button="Open" title="My Popup" %}
        {% async_lazy_popup name_button="Details" title="User Info" content_url="/my-app/user/42/" size="lg" %}
        {% async_lazy_popup name_button="Live Data" title="Always Fresh" always_reload_on_open=True %}
    """
    request = context.get("request")

    component_context = _build_modal_base_context(
        name_button, title, size, id_prefix="async-lazy-popup"
    )
    component_context["content_url"] = content_url or reverse("django_sample_components:lazy_popup_component")
    component_context["always_reload_on_open"] = always_reload_on_open

    return render_to_string(
        "django_sample_components/components/async_lazy_popup.html",
        component_context,
        request=request,
    )
