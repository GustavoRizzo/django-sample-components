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

Main submit endpoint:

- `POST /async/dynamic-forms/registration/component/`
- Returns the full component (`outerHTML` pattern).
- Triggers `showToast` via `HX-Trigger` header:
  - success: `"Registration submitted successfully!"`
  - error: `"Please fix the errors in the form."`

Per-field validation endpoints:

- `GET /async/dynamic-forms/registration/check-username/`
- `GET /async/dynamic-forms/registration/check-subject/`

Both endpoints:

- Require HTMX request headers.
- Return partial snippets used by the form.

## Example

```django
{% load async_tags %}

{% async_registration_form %}
```

## Notes

- Username check starts after user input is longer than 3 characters.
- Subject check reports full/almost-full/available states based on configured capacity.
