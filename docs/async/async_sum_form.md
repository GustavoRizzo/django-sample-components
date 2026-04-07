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
- Submit sends `POST` to ` /async/dynamic-forms/sum/component/`.
- The endpoint re-renders the full component via `outerHTML` swap.
- On valid submit, it triggers an HTMX event header with:
  - `showToast` message: `"Result calculated successfully!"`

## Example

```django
{% load async_tags %}

{% async_sum_form %}
```

## Notes

- Requires `django-crispy-forms` and `crispy-bootstrap5` configured in your project.
- The endpoint rejects non-HTMX requests with `400`.
