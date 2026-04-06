# `simple_popup`

A block tag that renders a Bootstrap 5 modal. The slot content (between the tags) is placed inside the modal body. The trigger button is rendered automatically.

Requires **Bootstrap JS** (`bootstrap.bundle.min.js`), included in the library's base template.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% simple_popup name_button [title] [size] [id_modal] [id_button]
               [use_layout_hiperlink] [class_button] %}
    ...modal body content...
{% endsimple_popup %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name_button` | `str` | — | Label of the button that opens the modal. |
| `title` | `str` | `"Popup Title"` | Title shown in the modal header. |
| `size` | `str` | `None` | Bootstrap modal size: `"sm"`, `"lg"`, or `"xl"`. Omitted if not set. |
| `id_modal` | `str` | Auto-generated | Custom HTML id for the modal element. |
| `id_button` | `str` | Derived from `id_modal` | Custom HTML id for the trigger button. |
| `use_layout_hiperlink` | `bool` | `False` | Renders the trigger as a styled hyperlink instead of a button. |
| `class_button` | `str` | `"btn btn-sm btn-outline-primary"` | Custom CSS classes for the trigger. Overrides `use_layout_hiperlink`. |

## Examples

```django
{# Basic popup #}
{% simple_popup name_button="Open" title="Hello" %}
    <p>This is the modal content.</p>
{% endsimple_popup %}

{# Large modal #}
{% simple_popup name_button="Open large" title="Details" size="lg" %}
    <p>Wide modal body.</p>
{% endsimple_popup %}

{# Trigger styled as a link #}
{% simple_popup name_button="View more" title="Info" use_layout_hiperlink=True %}
    <p>Content here.</p>
{% endsimple_popup %}

{# Custom button classes #}
{% simple_popup name_button="Delete" title="Confirm" class_button="btn btn-danger" %}
    <p>Are you sure?</p>
{% endsimple_popup %}

{# Nesting an async component inside the modal body #}
{% load sample_tags async_tags %}
{% simple_popup name_button="Open counter" title="Counter" size="sm" %}
    {% async_counter initial_value=0 step=1 %}
{% endsimple_popup %}
```

## Notes

- The modal element is moved to `<body>` via an inline `<script>` to avoid Bootstrap z-index issues when the component is nested inside positioned containers.
- `_build_modal_base_context` (defined in `simple_popup.py`) is the shared helper used by both `simple_popup` and async modal components. It handles ID generation and button class resolution.
