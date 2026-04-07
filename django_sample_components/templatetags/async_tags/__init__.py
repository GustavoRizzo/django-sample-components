from django import template

from .async_active_search import async_active_search
from .async_counter import async_counter
from .async_lazy_load import async_lazy_load
from .async_lazy_popup import async_lazy_popup
from .async_sum_form import async_sum_form

register = template.Library()

# Async tags
register.simple_tag(async_active_search, takes_context=True)
register.simple_tag(async_counter, takes_context=True)
register.simple_tag(async_lazy_load, takes_context=True)
register.simple_tag(async_lazy_popup, takes_context=True)
register.simple_tag(async_sum_form, takes_context=True)
