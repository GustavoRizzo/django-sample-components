
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

class SimpleAlertNode(template.Node):
    """Processes the block between {% simple_alert %} and {% endsimple_alert %}."""

    def __init__(self, nodelist: NodeList):
        self.nodelist = nodelist

    def render(self, context: RequestContext):
        # 1. Renderiza o conteúdo (o "slot") dentro do bloco.
        slot = self.nodelist.render(context)

        # 2. Prepara o contexto para o template base_alert.html
        render_context = {
            # Passa o conteúdo do slot como a variável 'slot'
            'slot': mark_safe(slot),
        }

        # 3. Renderiza o template final (o componente)
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
    Analisa a tag de bloco {% simple_alert %} ... {% endsimple_alert %}.
    """
    # Garante que não há argumentos (apenas o nome da tag)
    token.split_contents()

    # Captura o conteúdo até a tag de fechamento
    nodelist = parser.parse(('endsimple_alert',))
    parser.delete_first_token()  # Remove a tag de fechamento

    return SimpleAlertNode(nodelist)

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