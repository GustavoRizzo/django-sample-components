# `show_today_timestamp`

A simple tag that renders the current Unix timestamp as a string.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% show_today_timestamp %}
```

No parameters.

## Examples

```django
<p>Generated at: {% show_today_timestamp %}</p>
{# Output: Generated at: 1712345678 #}
```
