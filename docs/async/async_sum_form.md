# `async_sum_form`

An HTMX + crispy-forms component that sums two numbers without full-page reload.

## Load

```django
{% load async_tags %}
```

## Signature

```
{% async_sum_form %}
```

This tag takes no parameters.

## Endpoint flow

- Initial render comes from the tag template.
- Submit sends `POST` to `/async/dynamic-forms/sum/component/`.
- The endpoint re-renders the full component via `outerHTML` swap.
- On valid submit, triggers a `showToast` event: `"Result calculated successfully!"`
- On invalid submit, triggers a `showToast` event: `"Please fix the errors in the form."`

The view extends [`BaseFormComponentView`](base_form_component_view.md), so toast notifications and context injection are handled automatically.

## Context keys (template)

| Key | Present when | Description |
|---|---|---|
| `form` | always | The bound or unbound `SumForm` |
| `form_valid` | after successful submit | `True` |
| `form_invalid` | after failed submit | `True` |
| `result` | after successful submit | Computed sum value |

## Example

```django
{% load async_tags %}

{% async_sum_form %}
```

## Notes

- Requires `django-crispy-forms` and `crispy-bootstrap5` configured in your project.
- The endpoint rejects non-HTMX requests with `400`.
- Requires `{% simple_toast %}` somewhere in the page for toast notifications to appear.
