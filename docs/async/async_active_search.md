# `async_active_search`

A search input that filters results live on every keystroke. HTMX sends a `GET` request (debounced 300 ms) to the server and replaces a results table — no page reload.

Requires **HTMX** (included via pages that extend `master_async.html`).

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_active_search [search_url] [placeholder] [min_chars] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search_url` | `str` | Built-in demo endpoint | URL that handles search `GET` requests. |
| `placeholder` | `str` | `"Begin typing to search..."` | Input placeholder text. |
| `min_chars` | `int` | `1` | Minimum characters before search triggers. |

## HTMX behaviour

The input uses:
- `hx-trigger="input changed delay:300ms, keyup[key=='Enter'], load"` — debounced on input, immediate on Enter, and fires once on page load to populate initial results.
- `hx-target` pointing to the `<tbody>` inside the component.

## Custom endpoint

Your endpoint must:
1. Require the `HX-Request` header (return `400` otherwise).
2. Read the `search` query parameter.
3. Return `<tr>` rows matching the query.

```python
# views.py
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

CONTACTS = [
    {"first_name": "Alice", "last_name": "Johnson", "email": "alice@example.com"},
    # ...
]

class MySearchView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        query = request.GET.get("search", "").strip().lower()
        results = [
            c for c in CONTACTS
            if query in c["first_name"].lower() or query in c["email"].lower()
        ] if query else CONTACTS
        return render(request, "my_search_results.html", {"contacts": results})
```

```django
{# my_search_results.html #}
{% for contact in contacts %}
    <tr>
        <td>{{ contact.first_name }}</td>
        <td>{{ contact.last_name }}</td>
        <td>{{ contact.email }}</td>
    </tr>
{% empty %}
    <tr><td colspan="3" class="text-muted text-center">No results found.</td></tr>
{% endfor %}
```

## Examples

```django
{# Default — uses built-in demo data #}
{% async_active_search %}

{# Custom placeholder #}
{% async_active_search placeholder="Search by name or email..." %}

{# Point to your own endpoint #}
{% async_active_search search_url="/my-app/contacts/search/" placeholder="Find a contact..." %}
```

## Notes

- Each rendered instance gets a unique `id` — multiple instances on the same page are independent.
- The built-in endpoint searches 20 demo contacts by first name, last name, and email (case-insensitive).
- An empty search query returns all results.
