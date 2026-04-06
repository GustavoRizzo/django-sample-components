# `shout`

A block tag that renders its content as an uppercase `<h2>` with four exclamation marks appended.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% shout [bg_color] %}...{% endshout %}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bg_color` | `str` | No | `None` | CSS background color applied inline to the `<h2>` |

## Examples

```django
{% shout %}Let's go{% endshout %}
{# Output: <h2 style="text-transform:uppercase; background-color:None">Let's go!!!!</h2> #}

{% shout bg_color="#f0ad4e" %}Warning{% endshout %}
{# Output: <h2 style="text-transform:uppercase; background-color:#f0ad4e">Warning!!!!</h2> #}
```
