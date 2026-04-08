from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


class AsyncLazyPopupTemplateTagTests(SimpleTestCase):
    """Test the async_lazy_popup template tag rendering."""

    def test_renders_with_defaults(self):
        template = Template("{% load async_tags %}{% async_lazy_popup %}")
        rendered = template.render(Context())

        self.assertIn('async-lazy-popup-', rendered)
        self.assertIn('data-bs-toggle="modal"', rendered)
        self.assertIn('hx-get', rendered)

    def test_renders_custom_button_label(self):
        template = Template('{% load async_tags %}{% async_lazy_popup name_button="Open Details" %}')
        rendered = template.render(Context())

        self.assertIn('Open Details', rendered)

    def test_renders_custom_title(self):
        template = Template('{% load async_tags %}{% async_lazy_popup title="My Title" %}')
        rendered = template.render(Context())

        self.assertIn('My Title', rendered)

    def test_renders_custom_content_url(self):
        template = Template('{% load async_tags %}{% async_lazy_popup content_url="/my/url/" %}')
        rendered = template.render(Context())

        self.assertIn('/my/url/', rendered)

    def test_renders_size_modifier(self):
        template = Template('{% load async_tags %}{% async_lazy_popup size="lg" %}')
        rendered = template.render(Context())

        self.assertIn('modal-lg', rendered)

    def test_renders_no_size_modifier_by_default(self):
        template = Template("{% load async_tags %}{% async_lazy_popup %}")
        rendered = template.render(Context())

        self.assertNotIn('modal-sm', rendered)
        self.assertNotIn('modal-lg', rendered)
        self.assertNotIn('modal-xl', rendered)

    def test_renders_htmx_trigger_on_modal_show_event(self):
        template = Template("{% load async_tags %}{% async_lazy_popup %}")
        rendered = template.render(Context())

        self.assertIn('show.bs.modal', rendered)
        self.assertIn('hx-trigger', rendered)

    def test_renders_spinner_as_initial_content(self):
        template = Template("{% load async_tags %}{% async_lazy_popup %}")
        rendered = template.render(Context())

        self.assertIn('spinner-border', rendered)


class LazyPopupPageTests(SimpleTestCase):
    """Test the lazy-popup demo page."""

    url = reverse('lazy_popup')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b'htmx.min.js', response.content)

    def test_page_contains_component(self):
        response = self.client.get(self.url)
        self.assertIn(b'async-lazy-popup-', response.content)

    def test_page_contains_csrf_header(self):
        response = self.client.get(self.url)
        self.assertIn(b'X-CSRFToken', response.content)


class LazyPopupComponentTests(SimpleTestCase):
    """Test the lazy-popup HTMX endpoint (/async/lazy-popup/component/)."""

    url = reverse('django_sample_components:lazy_popup_component')

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_post_not_allowed(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 405)

    def test_get_with_htmx_returns_200(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)

    def test_response_contains_loaded_at(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'Loaded at', response.content)

    def test_response_contains_success_alert(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'alert-success', response.content)
