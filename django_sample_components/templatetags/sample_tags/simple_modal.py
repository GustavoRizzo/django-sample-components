from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def simple_modal(
    content: SafeString,
    id_modal: str,
    title: str = "Modal Title",
    size: str | None = None,
) -> SafeString:
    """
    Renders a Bootstrap 5 modal without a trigger button.

    Args:
        content:  HTML content rendered inside the modal body (block content).
        id_modal: HTML id for the modal element. Required — the caller must use this
                  same id in their trigger (data-bs-target="#<id_modal>").
        title:    Title displayed in the modal header. Default: "Modal Title".
        size:     Bootstrap modal size modifier: "sm", "lg", or "xl". Omitted if not set.
    """
    context = {
        "id_modal": id_modal,
        "title": title,
        "size": size,
        "slot": content,
    }
    return render_to_string("django_sample_components/components/simple_modal.html", context)
