from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def simple_toast(context, position: str = "bottom-end", autohide: bool = True, delay: int = 6000) -> SafeString:
    """Render a toast container with JS. Displays Django messages automatically and exposes window.showToast()."""
    position_map = {
        "top-start": "top-0 start-0",
        "top-center": "top-0 start-50 translate-middle-x",
        "top-end": "top-0 end-0",
        "bottom-start": "bottom-0 start-0",
        "bottom-center": "bottom-0 start-50 translate-middle-x",
        "bottom-end": "bottom-0 end-0",
    }
    return SafeString(
        render_to_string(
            "django_sample_components/components/simple_toast.html",
            {
                "toast_messages": list(context.get("messages", [])),
                "position_class": position_map.get(position, "bottom-0 end-0"),
                "autohide": autohide,
                "delay": delay,
            },
        )
    )
