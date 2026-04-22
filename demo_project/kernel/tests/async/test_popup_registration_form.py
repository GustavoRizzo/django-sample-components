from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


def popup_registration_form_tpl(tag_args: str = "") -> Template:
    """Build an async_popup_registration_form template string for testing."""
    return Template(
        "{% load async_tags %}"
        "{% async_popup_registration_form " + tag_args + " %}"
    )


class AsyncPopupRegistrationFormTemplateTagTests(SimpleTestCase):
    """Test the async_popup_registration_form template tag rendering."""

    def test_renders_modal_trigger_button(self):
        rendered = popup_registration_form_tpl().render(Context())

        self.assertIn("async-lazy-popup-", rendered)
        self.assertIn('data-bs-toggle="modal"', rendered)

    def test_renders_htmx_get(self):
        rendered = popup_registration_form_tpl().render(Context())

        self.assertIn("hx-get", rendered)
        self.assertIn("popup-registration/component/", rendered)

    def test_always_reload_on_open(self):
        rendered = popup_registration_form_tpl().render(Context())

        self.assertIn('hx-swap="innerHTML"', rendered)

    def test_default_button_label(self):
        rendered = popup_registration_form_tpl().render(Context())

        self.assertIn("Open Registration", rendered)

    def test_custom_button_label(self):
        rendered = popup_registration_form_tpl('name_button="Sign Up"').render(Context())

        self.assertIn("Sign Up", rendered)

    def test_custom_title(self):
        rendered = popup_registration_form_tpl('title="Create Account"').render(Context())

        self.assertIn("Create Account", rendered)

    def test_custom_size(self):
        rendered = popup_registration_form_tpl('size="lg"').render(Context())

        self.assertIn("modal-lg", rendered)

    def test_no_size_by_default(self):
        rendered = popup_registration_form_tpl().render(Context())

        self.assertNotIn("modal-sm", rendered)
        self.assertNotIn("modal-lg", rendered)
        self.assertNotIn("modal-xl", rendered)

    def test_renders_show_bs_modal_trigger(self):
        rendered = popup_registration_form_tpl().render(Context())

        self.assertIn("show.bs.modal", rendered)


class PopupRegistrationFormPageTests(SimpleTestCase):
    """Test the popup-registration demo page."""

    url = reverse("popup_registration_form")

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b"htmx.min.js", response.content)

    def test_page_contains_component(self):
        response = self.client.get(self.url)
        self.assertIn(b"async-lazy-popup-", response.content)

    def test_page_contains_csrf_header(self):
        response = self.client.get(self.url)
        self.assertIn(b"X-CSRFToken", response.content)


class PopupRegistrationFormComponentTests(SimpleTestCase):
    """Test the popup-registration HTMX endpoint."""

    url = reverse("django_sample_components:popup_registration_form_component")

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_post_not_allowed(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 405)

    def test_get_with_htmx_returns_200(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

    def test_response_contains_registration_form(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertIn(b"registration-form-wrapper", response.content)

    def test_response_contains_form_fields(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertIn(b"username", response.content)
        self.assertIn(b"subject", response.content)
