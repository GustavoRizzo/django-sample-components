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
├── templatetags/
│   ├── sample_tags/            # Static components ({% load sample_tags %})
│   │   ├── greeting.py             # Simple tag
│   │   ├── shout.py                # Block tag
│   │   ├── show_today_timestamp.py # Simple tag
│   │   ├── simple_alert.py         # Block tag — renders component template
│   │   ├── simple_button.py        # Simple tag — renders component template
│   │   ├── simple_popup.py         # Block tag — renders Bootstrap modal component
│   │   └── simple_typewriter.py    # Simple tag — renders component template
│   └── async_tags/             # HTMX-powered interactive components ({% load async_tags %})
│       └── async_counter.py        # Simple tag — counter with +/− buttons via HTMX
├── templates/django_sample_components/
│   ├── pages/                  # Demo/showcase pages (one per component)
│   ├── components/             # Component templates (alert, button, popup, typewriter, async_counter)
│   └── partials/               # Shared partials (menu, async partial responses)
├── static/                     # CSS/JS bundled with the package
├── views.py                    # CBVs for demo pages and async endpoints
├── urls.py                     # URL patterns for static components
└── async_urls.py               # URL patterns for async components (included under /async/)

demo_project/                   # Development/testing Django project
├── kernel/settings.py          # Installs django_sample_components
├── kernel/urls.py              # Routes all URLs to library's urls.py
└── kernel/tests/
    ├── test_loadpage.py        # Static component tests
    └── async/                  # Async component tests (one file per component)
        └── test_counter.py
```

**Component pattern:** Each component consists of a template tag in `templatetags/sample_tags/`, a template in `templates/django_sample_components/components/`, and optionally static assets. Block tags pass rendered content + context to a component template via `django.template.loader.render_to_string`.

**Template tag registration:** Tags are registered in `templatetags/sample_tags/__init__.py` using Django's `register = template.Library()` pattern. Consumers load them with `{% load sample_tags %}`.

## Async Components (HTMX)

Async components are intentionally kept separate from static components to allow extraction into a distinct Django app in the future. The separation boundaries are:

| Concern | Static | Async |
|---------|--------|-------|
| Template tags | `templatetags/sample_tags/` | `templatetags/async_tags/` |
| URL patterns | `urls.py` | `async_urls.py` (mounted at `/async/`) |
| Tests | `kernel/tests/test_*.py` | `kernel/tests/async/test_*.py` |

**Async URL pattern:** Each async component exposes a single URL (e.g. `/async/counter/`) that handles both `GET` (full demo page) and `POST` (HTMX partial response) in the same view. Use `request.htmx` to branch between the two responses — return `HttpResponseBadRequest()` if a POST arrives without the `HX-Request` header.

**Adding a new async component:** follow the same steps as static components, but place everything in the async equivalents: `async_tags/`, `async_urls.py`, and `kernel/tests/async/`.

**django-htmx:** the project uses [`django-htmx`](https://github.com/adamchainz/django-htmx) to integrate HTMX with Django. Key features used:

- `HtmxMiddleware` — adds `request.htmx` to every request. `bool(request.htmx)` is `True` when the request carries the `HX-Request` header.
- `{% htmx_script %}` — renders a `<script>` tag pointing to the htmx.js bundled with the package (no CDN dependency). The htmx version is determined by the installed `django-htmx` version.
- `{% django_htmx_script %}` — renders the Django↔HTMX integration script.
- CSRF is handled declaratively via `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on the `<body>` tag in `master_async.html` — no JavaScript event listener needed.

## Available Tags

| Tag | Type | Usage |
|-----|------|-------|
| `greeting` | simple_tag | `{% greeting %}` |
| `show_today_timestamp` | simple_tag | `{% show_today_timestamp %}` |
| `simple_typewriter` | simple_tag | `{% simple_typewriter words %}` |
| `simple_button` | simple_tag | `{% simple_button "Label" href="/url" btn_type="primary" %}` |
| `shout` | simple_block_tag | `{% shout %}...{% endshout %}` |
| `simple_alert` | simple_block_tag | `{% simple_alert type="info" %}...{% endsimple_alert %}` |
| `simple_popup` | simple_block_tag | `{% simple_popup name_button="Open" title="Title" %}...{% endsimple_popup %}` |

**`simple_popup` requires Bootstrap JS** (`bootstrap.bundle.min.js`) to open and close modals.

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
