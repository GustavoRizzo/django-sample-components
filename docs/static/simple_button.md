# `simple_button`

A simple tag that renders a Bootstrap anchor (`<a>`) styled as a button. Supports icons, tooltips, accessibility attributes, and arbitrary HTML attributes.

## Load

```django
{% load sample_tags %}
```

## Signature

```
{% simple_button text [href] [btn_type] [btn_size] [tooltip] [icon_before] [icon_after]
                 [extra_classes] [disabled] [new_tab] [nowrap] [aria_label] [hidden] %}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | — | Button label. Pass `""` for icon-only buttons. |
| `href` | `str` | `"#"` | Link URL. |
| `btn_type` | `str` | `"primary"` | Bootstrap color variant: `"primary"`, `"secondary"`, `"success"`, `"danger"`, `"warning"`, `"info"`, `"outline-primary"`, etc. |
| `btn_size` | `str` | `""` | Bootstrap size modifier: `"sm"`, `"lg"`, or `""` (default). |
| `tooltip` | `str` | `""` | Tooltip text shown on hover (Bootstrap tooltip). |
| `icon_before` | `str` | `""` | CSS classes for an `<i>` tag rendered before the label (e.g. `"fa fa-download"`). |
| `icon_after` | `str` | `""` | CSS classes for an `<i>` tag rendered after the label. |
| `extra_classes` | `str` | `""` | Additional CSS classes appended to the element. |
| `disabled` | `bool` | `False` | Renders the button as disabled. |
| `new_tab` | `bool` | `False` | Opens the link in a new tab (`target="_blank"`). |
| `nowrap` | `bool` | `True` | Prevents text wrapping (`text-nowrap`). |
| `aria_label` | `str` | `""` | Accessible label. Defaults to `text` when not provided. |
| `hidden` | `bool` | `False` | When `True`, renders nothing. |

Extra keyword arguments are rendered as HTML attributes on the `<a>` tag (e.g. `data_id="123"` → `data-id="123"`). Use `tooltip_placement` to control tooltip position: `"top"` (default), `"bottom"`, `"left"`, `"right"`.

## Examples

```django
{# Basic button #}
{% simple_button "Download" href="/files/report.pdf" %}

{# Outline variant, small, opens in new tab #}
{% simple_button "Docs" href="https://docs.example.com" btn_type="outline-secondary" btn_size="sm" new_tab=True %}

{# Icon before the label #}
{% simple_button "Save" icon_before="fa fa-save" btn_type="success" %}

{# Icon only (no label) #}
{% simple_button "" icon_before="fa fa-trash" btn_type="outline-danger" aria_label="Delete record" %}

{# With tooltip #}
{% simple_button "Export" tooltip="Download as CSV" icon_after="fa fa-download" %}

{# Disabled state #}
{% simple_button "Submit" disabled=True %}
```
