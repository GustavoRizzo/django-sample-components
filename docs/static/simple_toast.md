# `simple_toast`

A toast container component for Django messages, with a JavaScript API for manual toasts.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% simple_toast [position] [autohide] [delay] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `position` | `str` | `"bottom-end"` | Toast stack position. |
| `autohide` | `bool` | `True` | Whether to hide toasts automatically. |
| `delay` | `int` | `6000` | Auto-hide delay in milliseconds. |

Supported positions:

- `top-start`
- `top-center`
- `top-end`
- `bottom-start`
- `bottom-center`
- `bottom-end`

## Example

```django
{% load sample_tags %}

{# Render toasts from Django messages and expose window.showToast() #}
{% simple_toast position="bottom-end" autohide=True delay=5000 %}
```

## Notes

- The component reads messages from Django's `messages` framework.
- It also exposes a client-side helper (`window.showToast`) for custom runtime toasts.
