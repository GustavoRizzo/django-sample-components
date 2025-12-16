
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


from django import template
from django.template import NodeList, RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

# ----------------------------------------------------
# 1. Classe Node para Processar o Bloco
# ----------------------------------------------------

from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import NodeList, RequestContext

register = template.Library()

class SimpleAlertNode(template.Node):
    """Processes the block between {% simple_alert %} and {% endsimple_alert %}."""

    # 1. ADD 'prefix_text_expression' to __init__
    def __init__(self, nodelist: NodeList, prefix_text_expression=None):
        self.nodelist = nodelist
        self.prefix_text_expression = prefix_text_expression

    def render(self, context: RequestContext):
        # 1. Render the block content (the "slot")
        slot_content = self.nodelist.render(context)

        # 2. Resolve the value of the 'prefix_text' argument
        prefix_text = ""
        if self.prefix_text_expression:
            try:
                # Use resolve() to get the actual value (e.g., if it's a variable)
                prefix_text = self.prefix_text_expression.resolve(context)
            except template.VariableDoesNotExist:
                # Handle cases where the variable might not exist
                prefix_text = ""

        # 3. Prepare the context for the template
        render_context = {
            # Pass both the resolved prefix text and the slot content
            'prefix_text': prefix_text,
            'slot_content': mark_safe(slot_content),
        }

        # 4. Render the final template
        return render_to_string(
            'django_sample_components/components/simple_alert.html',
            render_context,
            request=context.get('request')
        )

# ----------------------------------------------------
# 2. Parser da Tag de Bloco
# ----------------------------------------------------

@register.tag(name='simple_alert')
def simple_alert_tag(parser, token):
    """
    Parses the block tag {% simple_alert [prefix_text="value"] %} ... {% endsimple_alert %}.
    """

    # Split all contents: ['simple_alert', 'prefix_text="Hello"']
    bits = token.split_contents()
    tag_name = bits[0]
    remaining_bits = bits[1:]

    prefix_text_expression = None

    if remaining_bits:
        if len(remaining_bits) > 1:
             raise template.TemplateSyntaxError(
                f"'{tag_name}' tag accepts only one optional argument: prefix_text=\"value\"."
            )

        # We expect the argument in key="value" format
        try:
            key, value = remaining_bits[0].split('=', 1)
        except ValueError:
            raise template.TemplateSyntaxError(
                f"Invalid argument format for '{tag_name}'. Expected format: prefix_text=\"value\"."
            )

        if key != 'prefix_text':
             raise template.TemplateSyntaxError(
                f"'{tag_name}' tag only accepts 'prefix_text' argument."
            )

        # Compile the filter (value) to handle variables/literals
        prefix_text_expression = parser.compile_filter(value)


    # Capture the content block until the closing tag
    nodelist = parser.parse(('endsimple_alert',))
    parser.delete_first_token()  # Remove the closing tag

    # 3. PASS 'prefix_text_expression' to the Node
    return SimpleAlertNode(nodelist, prefix_text_expression)

# from django import template

# register = template.Library()

# @register.tag(name="html_h1")
# def h1_tag(parser: Parser, token: Token):
#     nodelist = parser.parse(('endhtml_h1',))
#     parser.delete_first_token()

#     return HTML1Node(nodelist)

# class HTML1Node(template.Node):
#     def __init__(self, nodelist: NodeList):
#         self.nodelist = nodelist

#     def render(self, context: RequestContext):
#         output = self.nodelist.render(context)
#         return f"<h1>{output}</h1>"


@register.simple_block_tag
def alret_v2(
    content: SafeString,
    prefix_text: str
):
    """
    :param content: Content to display in the popup.
    :param name_button: Name of the button to trigger the popup.
    :param title: Title of the popup.
    :param id_modal: ID of the modal.
    :param use_layout_hiperlink: Whether to use layout hyperlink.
    """
    context = {
        'slot_content': content,
        'prefix_text': prefix_text,
    }
    return render_to_string('django_sample_components/components/simple_alert.html', context)