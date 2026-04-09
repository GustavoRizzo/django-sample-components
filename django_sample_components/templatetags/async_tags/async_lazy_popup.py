from django.template.loader import render_to_string
from django.utils.safestring import SafeString

from django_sample_components.templatetags.sample_tags.simple_popup import _build_modal_base_context


def async_lazy_popup(
    context,
    content: SafeString,
    name_button: str = "Open",
    title: str = "Popup Title",
    content_url: str = "",
    size: str | None = None,
    always_reload_on_open: bool = False,
) -> SafeString:
    """
    Renders a Bootstrap 5 modal that lazy-loads its body content via HTMX when opened.

    The block content is the initial placeholder displayed inside the modal while HTMX
    fetches the real content. The GET request to fetch the real content is triggered by
    the Bootstrap 'show.bs.modal' event, so the server is only called when the user
    actually opens the popup.

    Args:
        content:        Block content rendered as the initial placeholder (e.g. a loading spinner).
        name_button:    Label of the button that triggers the modal. Default: "Open".
        title:          Title displayed in the modal header. Default: "Popup Title".
        content_url:    URL to fetch the modal body content from. Required.
        size:           Bootstrap modal size modifier: "sm", "lg", or "xl". Omitted if not set.
        always_reload_on_open: When True, content is re-fetched every time the modal opens. When False
                        (default), content is fetched only on the first open — the HTMX trigger
                        element is removed from the DOM after the first load (outerHTML swap).

    Example:
        {% load async_tags %}
        {% async_lazy_popup name_button="Details" title="User Info" content_url="/my-app/user/42/" size="lg" %}
            <div class="spinner-border spinner-border-sm" role="status"></div>
        {% endasync_lazy_popup %}

        {% async_lazy_popup
            name_button="Live Data"
            title="Always Fresh"
            content_url="/my-app/live/"
            always_reload_on_open=True %}
            Loading...
        {% endasync_lazy_popup %}
    """
    request = context.get("request")

    component_context = _build_modal_base_context(
        name_button, title, size, id_prefix="async-lazy-popup"
    )
    component_context["content_url"] = content_url
    component_context["always_reload_on_open"] = always_reload_on_open
    component_context["slot"] = content

    return render_to_string(
        "django_sample_components/components/async_lazy_popup.html",
        component_context,
        request=request,
    )
