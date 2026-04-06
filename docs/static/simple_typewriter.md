# `simple_typewriter`

A simple tag that renders an animated typewriter effect cycling through a list of words.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% simple_typewriter words %}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `words` | `list[str]` | No | Built-in placeholder list | List of words/phrases to cycle through |

## Setup

The component bundles its own CSS and JavaScript. No extra configuration is needed when using the library's base template. If you use your own base template, make sure `collectstatic` has been run so the files are available.

## Examples

```django
{# Default placeholder words #}
{% simple_typewriter %}

{# Custom words from a Python list #}
{% simple_typewriter words %}

{# Inline list via a view context variable #}
{# In views.py: context = {"words": ["Fast", "Reliable", "Simple"]} #}
{% simple_typewriter words %}
```

### View example

```python
# views.py
class MyPage(View):
    def get(self, request):
        context = {
            "words": ["Fast", "Reliable", "Easy to use"],
        }
        return render(request, "my_page.html", context)
```

```django
{# my_page.html #}
{% load sample_tags %}
{% simple_typewriter words %}
```
