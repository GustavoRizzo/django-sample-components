from django import template

from .async_active_search import async_active_search
from .async_counter import async_counter
from .async_htmx_loader import async_htmx_loader
from .async_lazy_load import async_lazy_load
from .async_lazy_popup import async_lazy_popup
from .async_registration_form import async_registration_form
from .async_sum_form import async_sum_form

register = template.Library()

# Async tags
register.simple_tag(async_active_search, takes_context=True)
register.simple_tag(async_counter, takes_context=True)
register.simple_tag(async_htmx_loader, takes_context=True)
register.simple_tag(async_lazy_load, takes_context=True)
register.simple_block_tag(async_lazy_popup, takes_context=True)
register.simple_tag(async_registration_form, takes_context=True)
register.simple_tag(async_sum_form, takes_context=True)
