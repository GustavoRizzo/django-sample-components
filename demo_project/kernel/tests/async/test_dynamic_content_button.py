from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


def dcb_tpl(tag_args: str) -> Template:
    """Build an async_dynamic_content_button template string for testing."""
    return Template("{% load async_tags %}{% async_dynamic_content_button " + tag_args + " %}")


class AsyncDynamicContentButtonTemplateTagTests(SimpleTestCase):
    """Unit tests for the async_dynamic_content_button template tag."""

    def test_renders_hx_get_with_content_url(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertIn('hx-get="/my/url/"', rendered)

    def test_renders_hx_target_body(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertIn('hx-target="body"', rendered)

    def test_renders_hx_swap_beforeend(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertIn('hx-swap="beforeend"', rendered)

    def test_renders_default_button_label(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertIn('Open', rendered)

    def test_renders_custom_button_label(self):
        rendered = dcb_tpl('content_url="/my/url/" name_button="Delete"').render(Context())
        self.assertIn('Delete', rendered)

    def test_renders_default_class_button(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertIn('btn btn-sm btn-outline-primary', rendered)

    def test_renders_custom_class_button(self):
        rendered = dcb_tpl('content_url="/my/url/" class_button="btn btn-danger"').render(Context())
        self.assertIn('btn btn-danger', rendered)

    def test_renders_icon_when_provided(self):
        rendered = dcb_tpl('content_url="/my/url/" icon_button="bi bi-trash"').render(Context())
        self.assertIn('<i class="bi bi-trash">', rendered)

    def test_does_not_render_icon_by_default(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertNotIn('<i class=', rendered)

    def test_renders_button_type_button(self):
        rendered = dcb_tpl('content_url="/my/url/"').render(Context())
        self.assertIn('type="button"', rendered)


class DynamicContentButtonPageTests(SimpleTestCase):
    """Test the dynamic-content-button demo page."""

    url = reverse('dynamic_content_button')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b'htmx.min.js', response.content)

    def test_page_contains_csrf_header(self):
        response = self.client.get(self.url)
        self.assertIn(b'X-CSRFToken', response.content)

    def test_page_contains_hx_get(self):
        response = self.client.get(self.url)
        self.assertIn(b'hx-get', response.content)

    def test_page_contains_script_endpoint_url(self):
        response = self.client.get(self.url)
        self.assertIn(b'dynamic-content-button/script', response.content)

    def test_page_contains_modal_endpoint_url(self):
        response = self.client.get(self.url)
        self.assertIn(b'dynamic-content-button/modal', response.content)


class DynamicContentButtonScriptEndpointTests(SimpleTestCase):
    """Test the script HTMX endpoint (/async/dynamic-content-button/script/)."""

    url = reverse('django_sample_components:dynamic_content_button_script')

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_post_not_allowed(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 405)

    def test_get_with_htmx_returns_200(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)

    def test_response_contains_script_tag(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'<script>', response.content)

    def test_response_contains_closing_script_tag(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'</script>', response.content)


class DynamicContentButtonModalEndpointTests(SimpleTestCase):
    """Test the modal HTMX endpoint (/async/dynamic-content-button/modal/)."""

    url = reverse('django_sample_components:dynamic_content_button_modal')

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_post_not_allowed(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 405)

    def test_get_with_htmx_returns_200(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)

    def test_response_contains_modal_markup(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'class="modal fade"', response.content)

    def test_response_contains_modal_id(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'dcb-demo-modal', response.content)

    def test_response_contains_script_to_open_modal(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'Modal.getOrCreateInstance', response.content)

    def test_response_contains_cleanup_on_close(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn(b'hidden.bs.modal', response.content)
