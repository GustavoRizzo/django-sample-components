import uuid

from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def _build_modal_base_context(
    name_button: str,
    title: str,
    size: str | None,
    id_modal: str | None = None,
    id_button: str | None = None,
    id_prefix: str = "modal",
    use_layout_hiperlink: bool = False,
    class_button: str | None = None,
) -> dict:
    """Returns the shared context fields common to all modal components."""
    resolved_id_modal = id_modal if id_modal is not None else f"{id_prefix}-{uuid.uuid4()}"
    resolved_id_button = id_button if id_button is not None else f"{resolved_id_modal}-button"

    if class_button:
        resolved_class_button = class_button
    elif use_layout_hiperlink:
        resolved_class_button = "text-primary modern-link interactive"
    else:
        resolved_class_button = "btn btn-sm btn-outline-primary"

    return {
        "id_modal": resolved_id_modal,
        "id_button": resolved_id_button,
        "name_button": name_button,
        "title": title,
        "size": size,
        "use_layout_hiperlink": use_layout_hiperlink,
        "class_button": resolved_class_button,
    }


def simple_popup(
    content: SafeString,
    name_button: str,
    title: str = "Popup Title",
    id_modal: str = None,
    id_button: str = None,
    use_layout_hiperlink: bool = False,
    class_button: str = None,
    size: str | None = None,
) -> SafeString:
    """
    Renders a Bootstrap 5 modal triggered by a button.

    Args:
        content:              HTML content rendered inside the modal body (block content).
        name_button:          Label of the button that triggers the modal.
        title:                Title displayed in the modal header. Default: "Popup Title".
        id_modal:             Custom HTML id for the modal element. Auto-generated via uuid if omitted.
        id_button:            Custom HTML id for the trigger button. Derived from id_modal if omitted.
        use_layout_hiperlink: When True and class_button is not set, renders the trigger as a
                              styled hyperlink instead of a button. Default: False.
        class_button:         Custom CSS classes for the trigger element. Overrides use_layout_hiperlink.
                              Default: "btn btn-sm btn-outline-primary".
        size:                 Bootstrap modal size modifier: "sm", "lg", or "xl". Omitted if not set.
    """
    context = _build_modal_base_context(
        name_button, title, size, id_modal, id_button, use_layout_hiperlink, class_button
    )
    context["slot"] = content

    return render_to_string("django_sample_components/components/simple_popup.html", context)
