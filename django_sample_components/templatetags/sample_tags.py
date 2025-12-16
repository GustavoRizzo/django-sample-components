
import time

from django import template
from django.utils.safestring import mark_safe, SafeString
from django.template.loader import render_to_string

# Create an instance of the template library
register = template.Library()


# Use the simple_tag decorator to register the function as a template tag
@register.simple_tag
def show_today_timestamp():
    """
    Returns the current Unix timestamp (seconds since epoch).
    """
    # time.time() returns the timestamp as a float
    timestamp = int(time.time())

    # mark_safe is optional here, but it's good practice if the output were raw HTML
    return str(timestamp)


# --- Example of how you would do it if the tag needed arguments ---
@register.simple_tag
def greeting(name):
    """Returns a personalized greeting."""
    return f"Hello, {name}!"


@register.simple_block_tag
def shout(content: SafeString, bg_color):
    return mark_safe(f"<h2 style='text-transform:uppercase; background-color:{bg_color}'>{content}!!!!</h2>")


@register.simple_block_tag
def simple_alert(
    content: SafeString,
    type: str = 'info',
):
    """
    Renders a simple alert box with the given content and optional prefix text.
    Adds a Font Awesome icon based on the alert type.
    """
    match type:
        case 'info':
            alert_class = 'alert-info'
            text_class = 'text-info'
            icon_class = 'fa fa-info-circle'
        case 'warning':
            alert_class = 'alert-warning'
            text_class = 'text-warning'
            icon_class = 'fa fa-exclamation-triangle'
        case 'danger':
            alert_class = 'alert-danger'
            text_class = 'text-danger'
            icon_class = 'fa fa-times-circle'
        case 'success':
            alert_class = 'alert-success'
            text_class = 'text-success'
            icon_class = 'fa fa-check-circle'
        case _:
            alert_class = 'alert-info'
            text_class = 'text-info'
            icon_class = 'fa fa-info-circle'

    context = {
        'slot_content': content,
        'alert_class': alert_class,
        'text_class': text_class,
        'icon_class': icon_class,
    }
    return render_to_string('django_sample_components/components/simple_alert.html', context)
