from unittest.mock import MagicMock, patch

from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


class AsyncLazyLoadTemplateTagTests(SimpleTestCase):
    """Test the async_lazy_load template tag rendering."""

    def test_renders_with_defaults(self):
        template = Template("{% load async_tags %}{% async_lazy_load %}")
        rendered = template.render(Context())

        self.assertIn("async-lazy-load-", rendered)
        self.assertIn('hx-trigger="revealed once"', rendered)
        self.assertIn('hx-get="/async/lazy-load/"', rendered)

    def test_renders_custom_placeholder(self):
        template = Template('{% load async_tags %}{% async_lazy_load placeholder="Custom placeholder" %}')
        rendered = template.render(Context())

        self.assertIn("Custom placeholder", rendered)

    def test_renders_custom_url(self):
        template = Template('{% load async_tags %}{% async_lazy_load url="https://example.com/page" %}')
        rendered = template.render(Context())

        self.assertIn('hx-get="https://example.com/page"', rendered)

    def test_renders_delay_in_hx_vals(self):
        template = Template("{% load async_tags %}{% async_lazy_load delay_ms=1200 %}")
        rendered = template.render(Context())

        self.assertIn('"delay_ms": "1200"', rendered)


class AsyncLazyLoadPageTests(SimpleTestCase):
    """Test the lazy load demo page."""

    url = reverse("lazy_load_page")

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b"htmx.min.js", response.content)

    def test_page_contains_lazy_component(self):
        response = self.client.get(self.url)
        self.assertIn(b"async-lazy-load-", response.content)

    def test_page_contains_external_proxy_example(self):
        response = self.client.get(self.url)
        self.assertIn(b"/async/lazy-load/external/?target_url=https://www.google.com", response.content)


class AsyncLazyLoadPartialTests(SimpleTestCase):
    """Test the lazy load HTMX GET partial endpoint (/async/lazy-load/)."""

    url = reverse("django_sample_components:lazy_load")

    def test_lazy_load_partial_with_htmx(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Lazy content loaded!", response.content)
        self.assertIn(b"Loaded at:", response.content)

    @patch("django_sample_components.views.component.lazy_load_component.time.sleep")
    def test_lazy_load_partial_with_delay(self, sleep_mock):
        response = self.client.get(self.url, {"delay_ms": "250"}, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        sleep_mock.assert_called_once_with(0.25)


class AsyncLazyLoadExternalTests(SimpleTestCase):
    """Test the external lazy-load proxy endpoint (/async/lazy-load/external/)."""

    url = reverse("django_sample_components:lazy_load_external")

    def test_external_proxy_requires_htmx(self):
        response = self.client.get(self.url, {"target_url": "https://www.google.com"})
        self.assertEqual(response.status_code, 400)

    def test_external_proxy_rejects_invalid_scheme(self):
        response = self.client.get(self.url, {"target_url": "javascript:alert(1)"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 400)

    @patch("django_sample_components.views.component.lazy_load_external_component.urlopen")
    def test_external_proxy_fetches_title(self, urlopen_mock):
        mocked_response = MagicMock()
        mocked_response.read.return_value = b"<html><head><title>Google</title></head><body>ok</body></html>"
        urlopen_mock.return_value.__enter__.return_value = mocked_response

        response = self.client.get(self.url, {"target_url": "https://www.google.com"}, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"External lazy-load succeeded.", response.content)
        self.assertIn(b"Page title: Google", response.content)
