# django-sample-components

[![PyPI](https://img.shields.io/pypi/v/django-sample-components.svg)](https://pypi.org/project/django-sample-components/)

A reusable Django library that provides ready-to-use UI components — template tags, templates, and static assets — for use across Django projects.

Components are split into two groups:

- **Static** (`{% load sample_tags %}`) — pure server-side rendered components, no JavaScript dependencies beyond Bootstrap.
- **Async** (`{% load async_tags %}`) — interactive components powered by [HTMX](https://htmx.org/) that update without page reloads.


## Installation

```bash
pip install django-sample-components
# or
poetry add django-sample-components
```

Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_sample_components',
    'django_htmx',   # required for async components
]
```

Add `HtmxMiddleware` to `MIDDLEWARE` (required for async components):

```python
MIDDLEWARE = [
    # ...
    'django_htmx.middleware.HtmxMiddleware',
]
```

Include the library URLs in your project's `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    path('components/', include('django_sample_components.urls')),
]
```

In production, collect static files so your web server can serve them:

```bash
python manage.py collectstatic
```

> **Note:** This step is only required for production deployments. Django's development server (`runserver`) serves static files automatically from installed apps.


## Static Components

Load with `{% load sample_tags %}` in any template. No HTMX or JavaScript required (except Bootstrap JS for `simple_popup`).

| Tag | Type | Quick usage |
|-----|------|-------------|
| [`greeting`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/greeting.md) | simple_tag | `{% greeting "Alice" %}` |
| [`show_today_timestamp`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/show_today_timestamp.md) | simple_tag | `{% show_today_timestamp %}` |
| [`simple_typewriter`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/simple_typewriter.md) | simple_tag | `{% simple_typewriter words %}` |
| [`simple_button`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/simple_button.md) | simple_tag | `{% simple_button "Label" href="/url" btn_type="primary" %}` |
| [`simple_toast`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/simple_toast.md) | simple_tag | `{% simple_toast position="bottom-end" autohide=True delay=6000 %}` |
| [`shout`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/shout.md) | block_tag | `{% shout %}...{% endshout %}` |
| [`simple_alert`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/simple_alert.md) | block_tag | `{% simple_alert type="success" %}...{% endsimple_alert %}` |
| [`simple_popup`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/static/simple_popup.md) | block_tag | `{% simple_popup name_button="Open" title="Title" %}...{% endsimple_popup %}` |

### Quick example

```django
{% load sample_tags %}

{% simple_alert type="success" %}
    Your changes have been saved.
{% endsimple_alert %}

{% simple_popup name_button="Open" title="Confirm" size="sm" %}
    <p>Are you sure?</p>
{% endsimple_popup %}

{% simple_button "Download" href="/files/report.pdf" icon_before="fa fa-download" %}

{# Toast container for Django messages + JS API (window.showToast) #}
{% simple_toast position="bottom-end" autohide=True delay=5000 %}
```


## Async Components (HTMX)

Load with `{% load async_tags %}`. These components require HTMX and `django-htmx`. The easiest way to set them up is to extend `master_async.html`, which includes HTMX and handles CSRF automatically.

| Tag | Quick usage | Doc |
|-----|-------------|-----|
| [`async_counter`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_counter.md) | `{% async_counter initial_value=0 step=1 %}` | [docs](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_counter.md) |
| [`async_lazy_load`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_lazy_load.md) | `{% async_lazy_load url="/async/lazy-load/" delay_ms=1200 %}` | [docs](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_lazy_load.md) |
| [`async_active_search`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_active_search.md) | `{% async_active_search search_url="/search/" %}` | [docs](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_active_search.md) |
| [`async_lazy_popup`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_lazy_popup.md) | `{% async_lazy_popup name_button="Open" content_url="/content/" %}` | [docs](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_lazy_popup.md) |
| [`async_sum_form`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_sum_form.md) | `{% async_sum_form %}` | [docs](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_sum_form.md) |
| [`async_registration_form`](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_registration_form.md) | `{% async_registration_form %}` | [docs](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/async_registration_form.md) |

### Quick example

```django
{% load async_tags %}

{# Counter with step 5, bounded 0–100 #}
{% async_counter initial_value=0 step=5 min_value=0 max_value=100 %}

{# Live search against your own endpoint #}
{% async_active_search search_url="/contacts/search/" placeholder="Search contacts..." %}

{# Modal that loads content only when opened #}
{% async_lazy_popup name_button="View Report" title="Monthly Report"
                    content_url="/reports/monthly/" size="lg" %}

{# Lazy load any endpoint on reveal #}
{% async_lazy_load url="/async/counter/component/?initial_value=10&step=2" delay_ms=2000 %}

{# Async forms #}
{% async_sum_form %}
{% async_registration_form %}
```

### HTMX setup in your own base template

If you are not extending `master_async.html`, add the following to your base template:

```django
{% load django_htmx %}

<head>
    {% htmx_script %}
    {% django_htmx_script %}
</head>
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    ...
</body>
```


## Static vs Async — key differences

| | Static (`sample_tags`) | Async (`async_tags`) |
|---|---|---|
| Rendered | Server-side, with the page | On demand via HTMX |
| JavaScript | None (Bootstrap JS for popups) | HTMX required |
| Page reload | N/A | Never |
| Dependencies | Bootstrap CSS/JS | Bootstrap CSS/JS + HTMX + django-htmx |
| Best for | Simple UI elements | Interactive, live, or heavy-content components |


## Building your own async form components

The library exposes base classes and utilities to help you build HTMX form endpoints that integrate with the toast system.

### Base views (`django_sample_components.views.component.base`)

**`BaseFormComponentView`** — extends Django's `FormView`. Enforces the `HX-Request` header on POST, queues toast notifications automatically, and provides override hooks.

```python
from django_sample_components.views.component.base import BaseFormComponentView

class MyFormView(BaseFormComponentView):
    template_name = "myapp/components/my_form.html"
    form_class = MyForm
    success_message = "Saved!"
    error_message = "Please fix the errors."

    def get_success_context(self, form):
        ctx = super().get_success_context(form)
        ctx["result"] = form.compute_result()
        return ctx
```

**`BaseCreateFormComponentView`** — extends `BaseFormComponentView`. Calls `form.save()` on success and adds the created instance as `object` in the success context. Suitable for `ModelForm`-based components.

```python
from django_sample_components.views.component.base import BaseCreateFormComponentView

class MyModelFormView(BaseCreateFormComponentView):
    template_name = "myapp/components/my_model_form.html"
    form_class = MyModelForm
    success_message = "Record created!"
```

See [docs/async/base_form_component_view.md](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/async/base_form_component_view.md) for full reference.

### Toast utilities (`django_sample_components.utils`)

Helper functions to build `HX-Trigger` payloads that fire toast notifications in the browser via `showToast` / `showToasts` events.

```python
import json
from django_sample_components.utils import (
    get_json_show_toast,
    get_json_show_toasts,
    convert_django_messages_to_hx_triggers,
)

# Single toast
response["HX-Trigger"] = json.dumps(get_json_show_toast("Saved!", "success"))

# Multiple toasts at once
response["HX-Trigger"] = json.dumps(get_json_show_toasts([
    {"message": "Record saved.", "type": "success"},
    {"message": "Email notification sent.", "type": "info"},
]))

# Convert Django messages queue to HX-Trigger (used internally by BaseFormComponentView)
trigger = convert_django_messages_to_hx_triggers(request)
if trigger:
    response["HX-Trigger"] = json.dumps(trigger)
```

Valid toast types: `success`, `error`, `danger`, `warning`, `info`, `primary`, `secondary`.

See [docs/utils.md](https://github.com/GustavoRizzo/django-sample-components/blob/main/docs/utils.md) for full reference.


## Running locally

```bash
git clone https://github.com/GustavoRizzo/django-sample-components.git
cd django-sample-components
poetry install          # installs library + dev dependencies (includes demo extras)
poetry run task run-demo
```

Open `http://127.0.0.1:8000` to browse the component showcase.

> **Note:** The demo project uses [`django-simple-menu`](https://github.com/jazzband/django-simple-menu) for its navigation. This is a **dev-only** dependency — it is not installed when consumers add `django-sample-components` to their projects via `pip install` or `poetry add`.

### Tests

```bash
poetry run task test
```


## Publishing

```bash
poetry version patch   # bump version (e.g. 0.1.0 → 0.1.1)
poetry build
poetry publish
```

Update the version in both `pyproject.toml` and `django_sample_components/__init__.py` before releasing.
