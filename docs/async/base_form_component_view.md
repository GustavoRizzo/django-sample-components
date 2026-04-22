# `BaseFormComponentView` / `BaseCreateFormComponentView`

Base CBVs for building HTMX form component endpoints that integrate with the toast notification system.

## Import

```python
from django_sample_components.views.component.base import (
    BaseFormComponentView,
    BaseCreateFormComponentView,
)
```

## `BaseFormComponentView`

Extends Django's `FormView`. Designed for HTMX form endpoints where a component re-renders itself in place after submission.

### What it does automatically

1. Rejects non-HTMX POST requests with `400 Bad Request`.
2. On `form_valid`: queues a success Django message, calls `get_success_context`, renders the template, and attaches an `HX-Trigger` header with the toast payload.
3. On `form_invalid`: same flow with the error message and `get_error_context`.
4. Converts all queued Django messages to a single `HX-Trigger` header using `convert_django_messages_to_hx_triggers`.

### Class attributes

| Attribute | Default | Description |
|---|---|---|
| `success_message` | `"Operation completed successfully!"` | Message queued on valid submission |
| `error_message` | `"Please fix the errors in the form."` | Message queued on invalid submission |

### Override hooks

| Method | Purpose |
|---|---|
| `get_success_message()` | Override (return `None`) to suppress the success toast entirely |
| `get_error_message()` | Override (return `None`) to suppress the error toast entirely |
| `get_success_context(form)` | Add extra keys to the template context on success. Always call `super()` first |
| `get_error_context(form)` | Add extra keys to the template context on error. Always call `super()` first |

### Context keys injected automatically

| Key | Value |
|---|---|
| `form_valid` | `True` — present only on successful submission |
| `form_invalid` | `True` — present only on failed submission |

### Minimal example

```python
from django_sample_components.views.component.base import BaseFormComponentView
from myapp.forms import ContactForm

class ContactFormView(BaseFormComponentView):
    template_name = "myapp/components/contact_form.html"
    form_class = ContactForm
    success_message = "Message sent!"
```

### Customising context on success

```python
class SumFormView(BaseFormComponentView):
    template_name = "myapp/components/sum_form.html"
    form_class = SumForm
    success_message = "Result calculated!"

    def get_success_context(self, form):
        ctx = super().get_success_context(form)
        ctx["result"] = form.get_result()
        return ctx
```

### Suppressing the toast

```python
class SilentFormView(BaseFormComponentView):
    template_name = "myapp/components/silent_form.html"
    form_class = MyForm

    def get_success_message(self):
        return None  # no toast on success

    def get_error_message(self):
        return None  # no toast on error
```


## `BaseCreateFormComponentView`

Extends `BaseFormComponentView`. Adds `ModelForm` support — calls `form.save()` on success and makes the created instance available in the template context.

### Extra behaviour

- Calls `form.save()` before `get_success_context`.
- Adds `object` (the saved instance) to the success context.

### Example

```python
from django_sample_components.views.component.base import BaseCreateFormComponentView
from myapp.forms import ProductForm

class ProductFormView(BaseCreateFormComponentView):
    template_name = "myapp/components/product_form.html"
    form_class = ProductForm
    success_message = "Product created!"

    def get_success_context(self, form):
        ctx = super().get_success_context(form)
        # ctx["object"] is already set to the saved Product instance
        ctx["product_url"] = ctx["object"].get_absolute_url()
        return ctx
```

## URL registration

Both views are standard Django CBVs — register them as usual:

```python
# urls.py
from django.urls import path
from myapp.views import ContactFormView

urlpatterns = [
    path("contact/component/", ContactFormView.as_view(), name="contact-component"),
]
```

## Related

- [utils.md](../utils.md) — `convert_django_messages_to_hx_triggers` and other toast helpers used internally by these views.
- [async_sum_form.md](async_sum_form.md) — example component that uses `BaseFormComponentView`.
- [async_registration_form.md](async_registration_form.md) — example component that uses `BaseFormComponentView`.
