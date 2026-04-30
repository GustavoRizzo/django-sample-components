# `async_htmx_loader`

A generic HTMX `GET` loader with a Bootstrap spinner. Fires a request to a URL on a configurable trigger and replaces itself with the server response.

Requires **Bootstrap** (spinner) and **HTMX** (both included in `master_async.html`).

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_htmx_loader url_htmx [id_target] [hx_trigger] [hx_on_after_swap] [text_preload] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url_htmx` | `str` | — | URL fetched via HTMX `GET`. **Required.** |
| `id_target` | `str` | Auto-generated | HTML `id` for the target `<div>`. UUID-based if not provided. |
| `hx_trigger` | `str` | `"load"` | HTMX trigger expression (any valid `hx-trigger` value). |
| `hx_on_after_swap` | `str` | `None` | JS expression for `hx-on::after-swap`. Omitted when not provided. |
| `text_preload` | `str` | `"Loading, please wait..."` | Text shown alongside the spinner while the request is in-flight. |

## How it works

1. An outer `<div>` wraps an inner `<div id="<id_target>">` that carries the HTMX attributes.
2. On the configured trigger, HTMX sends a `GET` to `url_htmx` and replaces the inner `<div>` contents (`hx-swap="innerHTML"`) with the server response.
3. While waiting, a Bootstrap spinner and `text_preload` are displayed.

## Common triggers

| `hx_trigger` value | When it fires |
|---|---|
| `"load"` (default) | Immediately when the element is rendered in the page. |
| `"revealed once"` | When the element scrolls into the viewport (lazy load). Fires only once. |
| `"click"` | On user click. |
| `"every 5s"` | Polls every 5 seconds. |

## Examples

```django
{# Load immediately on page render #}
{% async_htmx_loader url_htmx="/async/counter/component/?initial_value=0" %}

{# Lazy-load on scroll-into-view #}
{% async_htmx_loader url_htmx="/api/heavy-data/" hx_trigger="revealed once" text_preload="Fetching data..." %}

{# Named target so you can reference it from other elements #}
{% async_htmx_loader url_htmx="/dashboard/stats/" id_target="stats-widget" %}

{# Run JS after the swap completes #}
{% async_htmx_loader url_htmx="/chart/data/" hx_on_after_swap="initChart()" %}
```

## Notes

- When `id_target` is omitted, a UUID-based id is generated at render time. Multiple instances on the same page will each have a unique id.
- The `hx_on_after_swap` expression is injected verbatim as `hx-on::after-swap="<expr>"` — keep it a simple JS expression (e.g. a function call), not a full statement block.
- The endpoint does not need to check for `HX-Request` unless you want to restrict direct access — the loader always sends the header.
