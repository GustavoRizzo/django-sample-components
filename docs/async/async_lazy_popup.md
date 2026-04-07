# `async_lazy_popup`

A Bootstrap 5 modal whose body content is fetched from the server via HTMX **only when the modal is opened**. The modal opens instantly with a loading spinner; the server is never called unless the user actually opens the popup.

Requires **Bootstrap JS** and **HTMX** (both included in `master_async.html`).

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_lazy_popup [name_button] [title] [content_url] [size] [always_reload_on_open] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name_button` | `str` | `"Open"` | Label of the trigger button. |
| `title` | `str` | `"Popup Title"` | Title shown in the modal header. |
| `content_url` | `str` | Built-in demo endpoint | URL fetched by HTMX when the modal opens. |
| `size` | `str` | `None` | Bootstrap modal size: `"sm"`, `"lg"`, or `"xl"`. |
| `always_reload_on_open` | `bool` | `False` | Controls whether content is fetched once or on every open (see below). |

## `always_reload_on_open`

| Value | `hx-swap` | Behaviour |
|-------|-----------|-----------|
| `False` (default) | `outerHTML` | Content is fetched **once**. After the first load, the HTMX trigger element is replaced by the content and removed from the DOM — no further requests are made on subsequent opens. |
| `True` | `innerHTML` | Content is re-fetched **every time** the modal opens. The trigger element persists in the DOM and fires on each `show.bs.modal` event. Useful for live data that must always be fresh. |

## How it works

1. User clicks the button → Bootstrap opens the modal immediately, showing a spinner.
2. Bootstrap fires the `show.bs.modal` event on the modal element.
3. HTMX listens for that event (`hx-trigger="show.bs.modal from:#<modal-id>"`) and sends a `GET` to `content_url`.
4. The server response replaces the spinner with real content.

## Custom endpoint

Your endpoint must require the `HX-Request` header (return `400` otherwise) and return an HTML fragment.

```python
# views.py
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

class MyPopupContent(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        context = {"user": request.user}
        return render(request, "my_popup_content.html", context)
```

## Examples

```django
{# Minimal — uses built-in demo endpoint #}
{% async_lazy_popup %}

{# Custom title and button label #}
{% async_lazy_popup name_button="View Details" title="User Profile" %}

{# Point to your own endpoint, large modal #}
{% async_lazy_popup name_button="Open" title="Report" content_url="/reports/summary/" size="lg" %}

{# Re-fetch content on every open (live data) #}
{% async_lazy_popup name_button="Live Stats" title="Dashboard" content_url="/stats/live/" always_reload_on_open=True %}

{# Load the async_counter component lazily inside a popup #}
{% async_lazy_popup name_button="Open Counter" title="Counter" content_url=counter_url size="sm" always_reload_on_open=True %}
```

### Loading `async_counter` lazily — view setup

```python
from django_sample_components.views.component.counter_component import CounterComponentView

class MyPage(View):
    def get(self, request):
        context = {
            "counter_url": CounterComponentView.get_url(initial_value=0, step=1),
        }
        return render(request, "my_page.html", context)
```

## Comparison: lazy vs regular popup

| | `async_lazy_popup` | `simple_popup` |
|---|---|---|
| Content loaded | On modal open | With the page |
| Server requests | 1 (or per-open with `always_reload_on_open`) | 0 (rendered server-side) |
| Use case | Heavy content, live data, rarely opened | Light content, always needed |
| Requires HTMX | Yes | No |

## Notes

- `async_lazy_popup` internally reuses `_build_modal_base_context` and the `simple_popup.html` template from the static component — the modal structure is identical.
- Each rendered instance gets a unique `id` (UUID-based) — multiple instances on the same page are fully independent.
