from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def async_dynamic_content_button(
    context,
    content_url: str,
    name_button: str = "Open",
    class_button: str = "btn btn-sm btn-outline-primary",
    icon_button: str | None = None,
) -> SafeString:
    """
    Renders a button that performs a GET to content_url via HTMX and appends the response
    to the end of <body>. The server response decides what happens: open a modal, inject
    a script, etc.

    Args:
        content_url:   URL fetched on click via hx-get. Required.
        name_button:   Button label. Default: "Open".
        class_button:  CSS classes applied to the button. Default: "btn btn-sm btn-outline-primary".
        icon_button:   Icon CSS classes rendered inside an <i> tag before the label (e.g.
                       "fa fa-plus", "bi bi-plus"). Omitted if not provided.

    Example:
        {% load async_tags %}
        {% async_dynamic_content_button content_url="/my-app/modal/" name_button="Add item" icon_button="bi bi-plus" %}
    """
    request = context.get("request")
    component_context = {
        "content_url": content_url,
        "name_button": name_button,
        "class_button": class_button,
        "icon_button": icon_button,
    }
    return render_to_string(
        "django_sample_components/components/async_dynamic_content_button.html",
        component_context,
        request=request,
    )
