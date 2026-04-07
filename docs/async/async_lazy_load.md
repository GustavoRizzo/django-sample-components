# `async_lazy_load`

A reveal-triggered lazy loader powered by HTMX.

The component sends a `GET` request only once (when it enters the viewport) and replaces itself with the server response.

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_lazy_load [url] [placeholder] [delay_ms] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `str` | `/async/lazy-load/` | Target URL fetched by HTMX. Can be internal or external. |
| `placeholder` | `str` | `"Scroll down to load content from the server."` | Placeholder text shown before content is loaded. |
| `delay_ms` | `int` | `None` | Optional delay sent to the endpoint in milliseconds. |

## HTMX behaviour

- `hx-trigger="revealed once"`
- `hx-get="{{ url }}"`
- `hx-swap="innerHTML"`
- Sends `delay_ms` in request params via `hx-vals`.

## Endpoints

Built-in endpoints:

- `GET /async/lazy-load/` — demo lazy-load response (supports optional `delay_ms`).
- `GET /async/lazy-load/external/?target_url=<url>` — server-side external fetch helper (supports optional `delay_ms`).

## Examples

```django
{# Default behavior #}
{% async_lazy_load %}

{# Custom placeholder #}
{% async_lazy_load placeholder="Waiting for reveal..." %}

{# Force 2 seconds delay #}
{% async_lazy_load delay_ms=2000 %}

{# Load full counter component lazily #}
{% async_lazy_load url="/async/counter/component/?initial_value=10&step=2" delay_ms=2000 %}

{# External URL through internal proxy #}
{% async_lazy_load
    url="/async/lazy-load/external/?target_url=https://www.google.com"
    placeholder="Loading external page through internal proxy..."
%}
```

## Notes

- For external pages, use the internal proxy endpoint (`/async/lazy-load/external/`) to avoid browser CORS limitations.
- Delay values are clamped server-side to keep responses predictable.
