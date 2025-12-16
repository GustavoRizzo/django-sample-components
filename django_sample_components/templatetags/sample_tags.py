
import time

from django import template
from django.utils.safestring import mark_safe, SafeString

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
