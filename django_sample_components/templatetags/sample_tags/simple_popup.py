import uuid

from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def simple_popup(
    content: SafeString,
    name_button: str,
    title: str = "Popup Title",
    id_modal: str = None,
    id_button: str = None,
    use_layout_hiperlink: bool = False,
    class_button: str = None,
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
    """
    def _button_class(class_button: str, use_layout_hiperlink: bool) -> str:
        if class_button:
            return class_button
        if use_layout_hiperlink:
            return "text-primary modern-link interactive"
        return "btn btn-sm btn-outline-primary"

    id_modal = f"modal-{uuid.uuid4()}" if id_modal is None else id_modal
    id_button = f"{id_modal}-button" if id_button is None else id_button

    context = {
        "id_modal": id_modal,
        "id_button": id_button,
        "title": title,
        "slot": content,
        "name_button": name_button,
        "use_layout_hiperlink": use_layout_hiperlink,
        "class_button": _button_class(class_button, use_layout_hiperlink),
    }
    return render_to_string("django_sample_components/components/simple_popup.html", context)
