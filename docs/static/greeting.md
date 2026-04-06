# `greeting`

A simple tag that returns a greeting string.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% greeting name %}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Name to greet |

## Examples

```django
{% greeting "Alice" %}
{# Output: Hello, Alice! #}

{% greeting user.first_name %}
{# Output: Hello, Bob! #}
```
