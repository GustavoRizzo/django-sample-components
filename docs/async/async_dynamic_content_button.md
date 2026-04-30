# `async_dynamic_content_button`

A button that performs a `GET` to a given URL via HTMX and appends the server response to the end of `<body>`. The server decides what to do with the response — open a modal, inject a script, etc.

Requires **HTMX** (included in `master_async.html`).

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_dynamic_content_button content_url [name_button] [class_button] [icon_button] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content_url` | `str` | — | URL fetched via `hx-get` on click. **Required.** |
| `name_button` | `str` | `"Open"` | Label displayed on the button. |
| `class_button` | `str` | `"btn btn-sm btn-outline-primary"` | CSS classes applied to the `<button>` element. |
| `icon_button` | `str` | `None` | Icon CSS classes rendered inside an `<i>` tag before the label (e.g. `"bi bi-plus"`, `"fa fa-plus"`). Omitted when not provided. |

## How it works

1. The button renders with `hx-get="<content_url>"` and `hx-target="body"` / `hx-swap="beforeend"`.
2. On click, HTMX sends a `GET` to `content_url` and appends the response HTML at the end of `<body>`.
3. The server controls the outcome — typical responses include an inline `<script>` that opens a modal or performs an action.

## Custom endpoint

The endpoint receives a standard `GET` with the `HX-Request` header. Return an HTML fragment (often a `<script>` tag or modal markup).

```python
# views.py
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

class MyContentView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        return render(request, "my_modal_fragment.html", {})
```

## Examples

```django
{# Minimal — just a URL #}
{% async_dynamic_content_button content_url="/my-app/modal/" %}

{# Custom label and icon #}
{% async_dynamic_content_button content_url="/items/add/" name_button="Add item" icon_button="bi bi-plus" %}

{# Override button style #}
{% async_dynamic_content_button content_url="/reports/export/" name_button="Export" class_button="btn btn-success" %}
```

## Notes

- The button uses `hx-swap="beforeend"` on `body` — any script tags returned by the server are executed immediately.
- For responses that open a Bootstrap modal, the server should return the modal HTML plus a short `<script>` that calls `new bootstrap.Modal(...)`.
- No `HX-Request` check is enforced on the client side; enforce it in your view if needed.
