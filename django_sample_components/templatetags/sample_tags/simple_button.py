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
    """
    Renders a Bootstrap anchor button (`<a>` tag styled as a button).

    Args:
        text:          Button label. Pass empty string for icon-only buttons.
        href:          URL the button links to. Default: "#".
        tooltip:       Tooltip text shown on hover (Bootstrap tooltip via data-bs-toggle).
        btn_type:      Bootstrap color variant. Examples: "primary", "secondary", "success",
                       "danger", "warning", "info", "light", "dark", "outline-primary",
                       "outline-secondary", etc. Default: "primary".
        btn_size:      Bootstrap size modifier. Options: "sm", "lg", or "" (default).
        extra_classes: Additional CSS classes appended to the button element.
        disabled:      Renders the button as disabled (adds `disabled` class and `aria-disabled`).
        icon_before:   Icon CSS classes rendered inside an `<i>` tag before the text.
                       Examples: "fa fa-download", "bi bi-download", "ti ti-download".
        icon_after:    Icon CSS classes rendered inside an `<i>` tag after the text.
        new_tab:       Opens the link in a new tab (`target="_blank"`).
        nowrap:        Prevents text wrapping (`text-nowrap`). Default: True.
        aria_label:    Accessible label. Defaults to `text` when not provided.
        hidden:        When True, renders nothing.
        **kwargs:      Extra HTML attributes rendered on the `<a>` tag (e.g. `data-id="123"`).
                       Use `tooltip_placement` to control tooltip position:
                       "top" (default), "bottom", "left", "right".
    """
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
