# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a reusable Django library (`django-sample-components`) that provides UI components (template tags, templates, static assets) for use across Django projects. It is published to PyPI and versioned with Poetry.

## Commands

All tasks are run via [taskipy](https://github.com/illBeRoy/taskipy) or directly:

```bash
# Linting
poetry run task lint          # ruff check
poetry run task lint-fix      # ruff check --fix

# Testing (runs Django test suite in demo_project)
poetry run task test

# Run demo server
poetry run task run-demo
# or: cd demo_project && python manage.py runserver

# Run a single test
cd demo_project && python manage.py test kernel.tests.test_loadpage.HomePageTests.test_home_page

# Collect static files (required after changing CSS/JS)
poetry run task collectstatic
```

## Architecture

```
django_sample_components/   # Installable package
├── urls/
│   ├── __init__.py              # Main URL patterns for static pages + /async include
│   ├── async_urls.py            # URL patterns for async pages/components (mounted at /async/)
│   └── dynamic_forms_urls.py    # Async URL subset for dynamic forms
├── templatetags/
│   ├── sample_tags/            # Static components ({% load sample_tags %})
│   │   ├── greeting.py             # Simple tag
│   │   ├── shout.py                # Block tag
│   │   ├── show_today_timestamp.py # Simple tag
│   │   ├── simple_alert.py         # Block tag — renders component template
│   │   ├── simple_button.py        # Simple tag — renders component template
│   │   ├── simple_popup.py         # Block tag — Bootstrap modal; exports _build_modal_base_context
│   │   ├── simple_toast.py         # Simple tag — toast container + JS API
│   │   └── simple_typewriter.py    # Simple tag — renders component template
│   └── async_tags/             # HTMX-powered interactive components ({% load async_tags %})
│       ├── async_counter.py        # Simple tag — counter with +/− buttons via HTMX
│       ├── async_active_search.py  # Simple tag — live search input via HTMX
│       ├── async_lazy_popup.py     # Simple tag — Bootstrap modal with lazy-loaded body via HTMX
│       ├── async_lazy_load.py      # Simple tag — reveal-triggered lazy loader via HTMX
│       ├── async_sum_form.py       # Simple tag — async sum form component
│       └── async_registration_form.py # Simple tag — async registration form component
├── templates/django_sample_components/
│   ├── pages/                  # Demo/showcase pages (one per component)
│   ├── components/             # Component templates
│   └── partials/               # Shared partials (menu, HTMX partial responses)
├── static/
│   ├── css/components/         # Per-component CSS (linked from component templates)
│   └── js/components/          # Per-component JS
├── views/
│   ├── __init__.py             # Public view exports
│   ├── pages.py                # CBVs for demo pages (all page classes use *Page suffix)
│   └── component/              # CBVs for HTMX endpoints (one file per component)

demo_project/                   # Development/testing Django project
├── kernel/settings.py          # Installs django_sample_components
├── kernel/urls.py              # Routes all URLs to library's urls.py
└── kernel/tests/
    ├── test_loadpage.py        # Static component tests
    └── async/                  # Async component tests (one file per component)
        ├── test_counter.py
        ├── test_active_search.py
        └── test_lazy_popup.py
```

**Component pattern:** Each component consists of a template tag in `templatetags/sample_tags/` (or `async_tags/`), a template in `templates/django_sample_components/components/`, and optionally a CSS file in `static/css/components/` linked via `<link>` inside the component template. Block tags pass rendered content + context to a component template via `django.template.loader.render_to_string`.

**CSS co-location:** Each component that requires custom CSS has its own file in `static/css/components/` (e.g. `async_counter.css`). The `<link>` tag is placed inside the component template itself (not in the page template), so consumers automatically get the styles when they use the tag. Run `poetry run task collectstatic` after adding or changing CSS files.

**Template tag registration:** Tags are registered in `templatetags/sample_tags/__init__.py` (or `async_tags/__init__.py`) using Django's `register = template.Library()` pattern.

## Async Components (HTMX)

Async components are intentionally kept separate from static components to allow extraction into a distinct Django app in the future. The separation boundaries are:

| Concern | Static | Async |
|---------|--------|-------|
| Template tags | `templatetags/sample_tags/` | `templatetags/async_tags/` |
| URL patterns | `urls/__init__.py` | `urls/async_urls.py` (mounted at `/async/`) |
| Tests | `kernel/tests/test_*.py` | `kernel/tests/async/test_*.py` |

**Dependency rule:** async components may import from static components (e.g. `async_lazy_popup` reuses `_build_modal_base_context` from `simple_popup`). The reverse is not allowed.

**Async URL pattern:** Each async component exposes two URLs — a page URL (full demo, no HTMX check) and a component URL (HTMX-only endpoint). The component endpoint returns `HttpResponseBadRequest()` if the `HX-Request` header is absent.

**Adding a new async component:** follow the same steps as static components, but place everything in the async equivalents: `async_tags/`, `urls/async_urls.py`, `views/component/`, and `kernel/tests/async/`.

**django-htmx:** the project uses [`django-htmx`](https://github.com/adamchainz/django-htmx) to integrate HTMX with Django. Key features used:

- `HtmxMiddleware` — adds `request.htmx` to every request. `bool(request.htmx)` is `True` when the request carries the `HX-Request` header.
- `{% htmx_script %}` — renders a `<script>` tag pointing to the htmx.js bundled with the package (no CDN dependency). The htmx version is determined by the installed `django-htmx` version.
- `{% django_htmx_script %}` — renders the Django↔HTMX integration script.
- CSRF is handled declaratively via `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on the `<body>` tag in `master_async.html` — no JavaScript event listener needed.

## Available Tags

### Static (`{% load sample_tags %}`)

| Tag | Type | Usage |
|-----|------|-------|
| `greeting` | simple_tag | `{% greeting %}` |
| `show_today_timestamp` | simple_tag | `{% show_today_timestamp %}` |
| `simple_typewriter` | simple_tag | `{% simple_typewriter words %}` |
| `simple_button` | simple_tag | `{% simple_button "Label" href="/url" btn_type="primary" %}` |
| `simple_toast` | simple_tag | `{% simple_toast position="bottom-end" autohide=True delay=6000 %}` |
| `shout` | simple_block_tag | `{% shout %}...{% endshout %}` |
| `simple_alert` | simple_block_tag | `{% simple_alert type="info" %}...{% endsimple_alert %}` |
| `simple_popup` | simple_block_tag | `{% simple_popup name_button="Open" title="Title" size="lg" %}...{% endsimple_popup %}` |

**`simple_popup`** accepts `size` (`"sm"`, `"lg"`, `"xl"`) for Bootstrap modal size. Requires Bootstrap JS. Internally uses `_build_modal_base_context` (importable by async tags).

### Async (`{% load async_tags %}`)

| Tag | Type | Usage |
|-----|------|-------|
| `async_counter` | simple_tag | `{% async_counter initial_value=0 step=1 min_value=0 max_value=10 %}` |
| `async_lazy_load` | simple_tag | `{% async_lazy_load url="/async/lazy-load/" delay_ms=1200 %}` |
| `async_active_search` | simple_tag | `{% async_active_search placeholder="Search..." min_chars=1 search_url="/custom/" %}` |
| `async_lazy_popup` | simple_tag | `{% async_lazy_popup name_button="Open" title="Title" content_url="/url/" size="lg" always_reload_on_open=True %}` |
| `async_sum_form` | simple_tag | `{% async_sum_form %}` |
| `async_registration_form` | simple_tag | `{% async_registration_form %}` |

**`async_counter`** — counter with +/− buttons. HTMX POSTs to `/async/counter/component/` on each click. Use `CounterComponentView.get_url(initial_value, step, min_value, max_value)` to generate the component URL programmatically.

**`async_active_search`** — search input that sends a GET to `search_url` on every keystroke (debounced 300 ms). The endpoint must accept a `search` query param and return `<tr>` rows. Returns `HttpResponseBadRequest` without `HX-Request` header.

**`async_lazy_popup`** — Bootstrap modal whose body is fetched via HTMX only when the modal opens (triggered by `show.bs.modal`). Key parameters:
- `content_url` — URL to fetch; defaults to the built-in demo endpoint.
- `size` — Bootstrap modal size modifier (`"sm"`, `"lg"`, `"xl"`).
- `always_reload_on_open` — when `False` (default) content is fetched once and the trigger element is removed from the DOM (`hx-swap="outerHTML"`). When `True`, content is re-fetched on every open (`hx-swap="innerHTML"`). Useful for live data.

**`async_lazy_load`** — reveal-triggered lazy loader that performs a one-time HTMX `GET` (`hx-trigger="revealed once"`). Supports custom `url`, placeholder text, and optional `delay_ms`.

**`async_sum_form`** — interactive sum form built with crispy-forms. Posts to `/async/dynamic-forms/sum/component/` and updates in place.

**`async_registration_form`** — interactive registration form with per-field HTMX validation (`username` and `subject`) and toast triggers on submit.

## Versioning & Publishing

Version is defined in `pyproject.toml`. Update it there and in `django_sample_components/__init__.py` before releasing.

```bash
poetry build
poetry publish
```

## Code Style

- Line length: 120 characters (ruff)
- Active ruff rules: F, E, W, I, N, UP, B
- Type checking: mypy
- **Language: all code, comments, docstrings, and template text must be written in English.**

## Template Style

- Use `{# ... #}` for inline comments in Django templates. Reserve `{% comment %}...{% endcomment %}` only for multi-line block comments.
