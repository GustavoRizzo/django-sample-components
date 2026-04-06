import uuid

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import SafeString


def async_lazy_popup(
    context,
    name_button: str = "Open",
    title: str = "Popup Title",
    content_url: str | None = None,
    size: str | None = None,
) -> SafeString:
    """
    Renders a Bootstrap 5 modal that lazy-loads its body content via HTMX when opened.

    The modal opens instantly with a loading spinner. The GET request to fetch the real
    content is triggered by the Bootstrap 'show.bs.modal' event, so the server is only
    called when the user actually opens the popup.

    Args:
        name_button:  Label of the button that triggers the modal. Default: "Open".
        title:        Title displayed in the modal header. Default: "Popup Title".
        content_url:  URL to fetch the modal body content from. Defaults to the built-in demo endpoint.
        size:         Bootstrap modal size modifier: "sm", "lg", or "xl". Omitted if not set.

    Example:
        {% load async_tags %}
        {% async_lazy_popup name_button="Open" title="My Popup" %}
        {% async_lazy_popup name_button="Details" title="User Info" content_url="/my-app/user/42/" size="lg" %}
    """
    request = context.get("request")
    id_modal = f"async-lazy-popup-{uuid.uuid4()}"

    component_context = {
        "id_modal": id_modal,
        "id_button": f"{id_modal}-button",
        "name_button": name_button,
        "title": title,
        "content_url": content_url or reverse("django_sample_components:lazy_popup_component"),
        "size": size,
    }

    return render_to_string(
        "django_sample_components/components/async_lazy_popup.html",
        component_context,
        request=request,
    )
