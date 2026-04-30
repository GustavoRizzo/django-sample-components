# `async_popup_registration_form`

A Bootstrap 5 modal button that lazy-loads the registration form when the modal opens. Built on top of [`async_lazy_popup`](async_lazy_popup.md) with `always_reload_on_open=True`, so the user always starts with a fresh, empty form.

Requires **Bootstrap JS** and **HTMX** (both included in `master_async.html`).

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_popup_registration_form [name_button] [title] [size] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name_button` | `str` | `"Open Registration"` | Label of the button that triggers the modal. |
| `title` | `str` | `"Registration Form"` | Title displayed in the modal header. |
| `size` | `str` | `None` | Bootstrap modal size modifier: `"sm"`, `"lg"`, or `"xl"`. Omitted if not set. |

## How it works

This tag is a thin wrapper around `async_lazy_popup` that points `content_url` at the built-in registration form endpoint (`/async/dynamic-forms/registration/popup-component/`) and sets `always_reload_on_open=True`. The form is re-fetched on every modal open, ensuring a clean state.

See [`async_registration_form`](async_registration_form.md) for full endpoint details, validation rules, and toast behaviour.

## Examples

```django
{# Default button and title #}
{% async_popup_registration_form %}

{# Custom label and title #}
{% async_popup_registration_form name_button="Register" title="Sign Up" %}

{# Large modal #}
{% async_popup_registration_form name_button="Create Account" title="New User" size="lg" %}
```

## Notes

- Requires `{% simple_toast %}` somewhere in the page for toast notifications triggered by the form to appear.
- The form endpoint rejects non-HTMX requests with `400`.
- Each rendered instance gets a unique modal `id` — multiple instances on the same page work independently.
