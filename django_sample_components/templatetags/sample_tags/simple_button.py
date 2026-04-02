from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def simple_button(
    text: str,
    href: str = "#",
    tooltip: str = "",
    btn_type: str = "primary",
    btn_size: str = "",
    extra_classes: str = "",
    disabled: bool = False,
    icon_before: str = "",
    icon_after: str = "",
    new_tab: bool = False,
    nowrap: bool = True,
    aria_label: str = "",
    hidden: bool = False,
    **kwargs,
) -> SafeString:
    context = {
        "text": text,
        "href": href,
        "tooltip": tooltip,
        "btn_type": btn_type,
        "btn_size": btn_size,
        "extra_classes": extra_classes,
        "disabled": disabled,
        "icon_before": icon_before,
        "icon_after": icon_after,
        "new_tab": new_tab,
        "nowrap": nowrap,
        "aria_label": aria_label,
        "hidden": hidden,
        "kwargs": kwargs,
    }
    return render_to_string(
        "django_sample_components/components/simple_button.html", context)
