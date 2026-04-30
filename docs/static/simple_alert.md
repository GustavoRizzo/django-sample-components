# `simple_alert`

A block tag that renders a Bootstrap alert box with an icon determined by the alert type.

Requires **Font Awesome** (included in the library's master template).

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% simple_alert [type] [close_button] %}...{% endsimple_alert %}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `type` | `str` | No | `"info"` | Alert variant. Options: `"info"`, `"warning"`, `"danger"`, `"success"` |
| `close_button` | `bool` | No | `True` | Whether to render the close button (`btn-close`). |

## Examples

```django
{% simple_alert %}
    Your session will expire in 5 minutes.
{% endsimple_alert %}

{% simple_alert type="success" %}
    Your changes have been saved.
{% endsimple_alert %}

{% simple_alert type="danger" %}
    An error occurred. Please try again.
{% endsimple_alert %}

{% simple_alert type="warning" %}
    This action cannot be undone.
{% endsimple_alert %}

{% simple_alert type="info" close_button=False %}
    Informational alert without a close button.
{% endsimple_alert %}
```

## Alert Types

| `type` | Bootstrap class | Font Awesome icon |
|--------|----------------|-------------------|
| `"info"` | `alert-info` | `fa-info-circle` |
| `"warning"` | `alert-warning` | `fa-exclamation-triangle` |
| `"danger"` | `alert-danger` | `fa-times-circle` |
| `"success"` | `alert-success` | `fa-check-circle` |
