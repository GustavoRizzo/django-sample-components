from django import template

from .async_counter import async_counter
from .async_lazy_load import async_lazy_load

register = template.Library()

# Async tags
register.simple_tag(async_counter, takes_context=True)
register.simple_tag(async_lazy_load, takes_context=True)
