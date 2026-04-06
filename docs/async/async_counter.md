# `async_counter`

An interactive counter with `+` and `−` buttons. Each click sends an HTMX `POST` request to the server and replaces the component in place — no page reload.

Requires **HTMX** (included via `{% load async_tags %}` pages that extend `master_async.html`).

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_counter [initial_value] [step] [min_value] [max_value] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_value` | `int` | `0` | Starting value of the counter. |
| `step` | `int` | `1` | Amount added or subtracted on each click. |
| `min_value` | `int` | `None` | Minimum allowed value. No lower limit if omitted. |
| `max_value` | `int` | `None` | Maximum allowed value. No upper limit if omitted. |

## HTMX endpoint

`POST /async/counter/component/`

The endpoint also accepts `GET` requests (with `HX-Request` header) to render a fresh counter — used when loading the component via lazy popup or other HTMX triggers.

Use `CounterComponent.get_url()` to build the GET URL programmatically:

```python
from django_sample_components.views.component.counter_component import CounterComponent

url = CounterComponent.get_url(initial_value=5, step=2, min_value=0, max_value=20)
# → /async/counter/component/?initial_value=5&step=2&min_value=0&max_value=20
```

## Examples

```django
{# Basic counter starting at 0 #}
{% async_counter %}

{# Start at 10, step by 5 #}
{% async_counter initial_value=10 step=5 %}

{# Bounded counter: 0–100 #}
{% async_counter initial_value=50 step=1 min_value=0 max_value=100 %}

{# Multiple independent counters on the same page #}
{% async_counter initial_value=0 step=1 %}
{% async_counter initial_value=0 step=10 min_value=0 max_value=100 %}
```

## Notes

- Each rendered counter gets a unique `id` (UUID-based), so multiple instances on the same page are fully independent.
- The server enforces `min_value` / `max_value` — the frontend passes them on every request so limits are always respected, even if the user inspects and modifies the DOM.
