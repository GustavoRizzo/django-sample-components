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

Collect static files:

```bash
python manage.py collectstatic
```


## Static Components

Load with `{% load sample_tags %}` in any template. No HTMX or JavaScript required (except Bootstrap JS for `simple_popup`).

| Tag | Type | Quick usage |
|-----|------|-------------|
| [`greeting`](docs/static/greeting.md) | simple_tag | `{% greeting "Alice" %}` |
| [`show_today_timestamp`](docs/static/show_today_timestamp.md) | simple_tag | `{% show_today_timestamp %}` |
| [`simple_typewriter`](docs/static/simple_typewriter.md) | simple_tag | `{% simple_typewriter words %}` |
| [`simple_button`](docs/static/simple_button.md) | simple_tag | `{% simple_button "Label" href="/url" btn_type="primary" %}` |
| [`shout`](docs/static/shout.md) | block_tag | `{% shout %}...{% endshout %}` |
| [`simple_alert`](docs/static/simple_alert.md) | block_tag | `{% simple_alert type="success" %}...{% endsimple_alert %}` |
| [`simple_popup`](docs/static/simple_popup.md) | block_tag | `{% simple_popup name_button="Open" title="Title" %}...{% endsimple_popup %}` |

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
```


## Async Components (HTMX)

Load with `{% load async_tags %}`. These components require HTMX and `django-htmx`. The easiest way to set them up is to extend `master_async.html`, which includes HTMX and handles CSRF automatically.

| Tag | Quick usage | Doc |
|-----|-------------|-----|
| [`async_counter`](docs/async/async_counter.md) | `{% async_counter initial_value=0 step=1 %}` | [docs](docs/async/async_counter.md) |
| [`async_active_search`](docs/async/async_active_search.md) | `{% async_active_search search_url="/search/" %}` | [docs](docs/async/async_active_search.md) |
| [`async_lazy_popup`](docs/async/async_lazy_popup.md) | `{% async_lazy_popup name_button="Open" content_url="/content/" %}` | [docs](docs/async/async_lazy_popup.md) |

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


## Running locally

```bash
git clone https://github.com/GustavoRizzo/django-sample-components.git
cd django-sample-components
poetry install
poetry run task run-demo
```

Open `http://127.0.0.1:8000` to browse the component showcase.

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
