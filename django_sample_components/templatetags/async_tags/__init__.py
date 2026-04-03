from django import template

from .async_counter import async_counter

register = template.Library()

# Async tags
register.simple_tag(async_counter, takes_context=True)
