# Toast utilities (`django_sample_components.utils`)

Helper functions for building `HX-Trigger` response headers that fire toast notifications in the browser.

These utilities depend on the `simple_toast` component being present in the page — it registers the `showToast` / `showToasts` JavaScript event listeners.

## Import

```python
from django_sample_components.utils import (
    get_json_show_toast,
    get_json_show_toasts,
    convert_django_messages_to_hx_triggers,
)
```

## Valid toast types

`success`, `error`, `danger`, `warning`, `info`, `primary`, `secondary`

Passing an invalid type raises `ValueError`.

---

## `get_json_show_toast(message, toast_type)`

Returns a dict suitable for `json.dumps` that triggers a **single** toast.

```python
import json
response["HX-Trigger"] = json.dumps(get_json_show_toast("Saved!", "success"))
# → HX-Trigger: {"showToast": {"message": "Saved!", "type": "success"}}
```

| Parameter | Type | Description |
|---|---|---|
| `message` | `str` | Text shown in the toast |
| `toast_type` | `str` | One of the valid toast types above |

---

## `get_json_show_toasts(items)`

Returns a dict that triggers **multiple** toasts at once using the `showToasts` event (avoids duplicate-key collisions in JSON).

```python
import json
response["HX-Trigger"] = json.dumps(get_json_show_toasts([
    {"message": "Record saved.", "type": "success"},
    {"message": "Email notification queued.", "type": "info"},
]))
# → HX-Trigger: {"showToasts": [{"message": "...", "type": "success"}, ...]}
```

| Parameter | Type | Description |
|---|---|---|
| `items` | `list[dict]` | Each dict must have `"message"` (str) and `"type"` (valid toast type) |

---

## `convert_django_messages_to_hx_triggers(request)`

Consumes all messages in Django's messages queue for the current request and returns the appropriate `HX-Trigger` payload dict.

| Messages queued | Returns |
|---|---|
| 0 | `{}` (empty — do not set the header) |
| 1 | `{"showToast": {...}}` |
| 2+ | `{"showToasts": [...]}` |

```python
import json
from django_sample_components.utils import convert_django_messages_to_hx_triggers

# In a view:
from django.contrib import messages
messages.success(request, "Done!")
messages.warning(request, "Check the report for warnings.")

trigger = convert_django_messages_to_hx_triggers(request)
response = render(request, "myapp/component.html", context)
if trigger:
    response["HX-Trigger"] = json.dumps(trigger)
```

> This function is called automatically by `BaseFormComponentView`. Use it directly only in custom views that manage Django messages manually.

### Django tag → toast type mapping

| Django message tag | Toast type |
|---|---|
| `debug` | `info` |
| `info` | `info` |
| `success` | `success` |
| `warning` | `warning` |
| `error` | `error` |

---

## Full view example

```python
import json
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django_sample_components.utils import get_json_show_toast

class MyComponentView(View):
    def post(self, request):
        if not request.htmx:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

        # ... process logic ...

        response = render(request, "myapp/component.html", {"done": True})
        response["HX-Trigger"] = json.dumps(get_json_show_toast("Done!", "success"))
        return response
```

## Related

- [base_form_component_view.md](async/base_form_component_view.md) — base CBVs that use these utilities internally.
- [simple_toast](static/simple_toast.md) — the template tag that registers the `showToast` / `showToasts` event listeners on the page.
