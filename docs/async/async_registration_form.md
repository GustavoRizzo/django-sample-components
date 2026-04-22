# `async_registration_form`

A registration form component with per-field HTMX validation and submit-time feedback.

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_registration_form %}
```

This tag takes no parameters.

## Endpoint flow

The main submit view extends [`BaseFormComponentView`](base_form_component_view.md), so toast notifications and context injection are handled automatically.

**Main submit endpoint:**

- `POST /async/dynamic-forms/registration/component/`
- Re-renders the full component via `outerHTML` swap.
- On success: triggers `showToast` — `"Registration submitted successfully!"`
- On error: triggers `showToast` — `"Please fix the errors in the form."`

**Per-field validation endpoints:**

| Endpoint | Trigger | Behaviour |
|---|---|---|
| `GET /async/dynamic-forms/registration/check-username/` | `hx-trigger="keyup changed delay:400ms"` on username field | Returns a partial snippet when `len(username) > 3` |
| `GET /async/dynamic-forms/registration/check-subject/` | `hx-trigger="change"` on subject field | Returns a partial snippet with capacity status |

Both validation endpoints require the `HX-Request` header — return `400` otherwise.

## Context keys (template)

| Key | Present when | Description |
|---|---|---|
| `form` | always | The bound or unbound `RegistrationForm` |
| `form_valid` | after successful submit | `True` |
| `form_invalid` | after failed submit | `True` |
| `success` | after successful submit | `True` — use to show a confirmation message in the template |

## Username validation rules

- Check triggers only when `len(username) > 3`.
- Returns "Username is available." or "That username is already taken."

## Subject validation rules

- Returns one of three states based on `SUBJECT_CAPACITY`:
  - **Full** — 0 spots remaining → invalid message.
  - **Almost full** — ≤ 3 spots remaining → warning message.
  - **Available** — shows remaining spot count.

## Example

```django
{% load async_tags %}

{% async_registration_form %}
```

## Notes

- Requires `{% simple_toast %}` somewhere in the page for toast notifications to appear.
- The endpoint rejects non-HTMX POST requests with `400`.
- `TAKEN_USERNAMES` and `SUBJECT_CAPACITY` are demo fixtures defined in `forms/registration_form.py` — replace with real database queries in production use.
