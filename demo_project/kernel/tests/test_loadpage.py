from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    """Test class to verify the home page is accessible."""
    app_name = 'django_sample_components'

    home_page_url = reverse(f"{app_name}:home")
    greeting_page_url = reverse(f"{app_name}:greeting")
    alert_page_url = reverse(f"{app_name}:alert")
    popup_page_url = reverse(f"{app_name}:popup")

    def test_home_page_status_code(self):
        response = self.client.get(self.home_page_url)
        self.assertEqual(response.status_code, 200)

    def test_greeting_page_status_code(self):
        response = self.client.get(self.greeting_page_url)
        self.assertEqual(response.status_code, 200)

    def test_alert_page_status_code(self):
        response = self.client.get(self.alert_page_url)
        self.assertEqual(response.status_code, 200)

    def test_popup_page_status_code(self):
        response = self.client.get(self.popup_page_url)
        self.assertEqual(response.status_code, 200)


class ToastPageTests(SimpleTestCase):
    """Test the toast demo page."""

    toast_page_url = reverse("django_sample_components:toast")

    def test_page_status_code(self):
        response = self.client.get(self.toast_page_url)
        self.assertEqual(response.status_code, 200)

    def test_page_renders_toast_container(self):
        response = self.client.get(self.toast_page_url)
        self.assertContains(response, 'id="toast-container"')
        self.assertContains(response, 'showToast')


class SimpleToastTemplateTagTests(SimpleTestCase):
    """Test the simple_toast template tag rendering."""

    def test_renders_toast_container(self):
        template = Template('{% load sample_tags %}{% simple_toast %}')
        rendered = template.render(Context())
        self.assertIn('id="toast-container"', rendered)
        self.assertIn('showToast', rendered)

    def test_default_position_bottom_end(self):
        template = Template('{% load sample_tags %}{% simple_toast %}')
        rendered = template.render(Context())
        self.assertIn('bottom-0 end-0', rendered)

    def test_custom_position_top_end(self):
        template = Template('{% load sample_tags %}{% simple_toast position="top-end" %}')
        rendered = template.render(Context())
        self.assertIn('top-0 end-0', rendered)


class SimplePopupTemplateTagTests(SimpleTestCase):
    """Test the simple_popup template tag rendering."""

    def test_renders_size_modifier(self):
        template = Template(
            '{% load sample_tags %}{% simple_popup name_button="Open" size="lg" %}content{% endsimple_popup %}'
        )
        rendered = template.render(Context())

        self.assertIn('modal-lg', rendered)

    def test_renders_no_size_class_by_default(self):
        template = Template('{% load sample_tags %}{% simple_popup name_button="Open" %}content{% endsimple_popup %}')
        rendered = template.render(Context())

        self.assertNotIn('modal-sm', rendered)
        self.assertNotIn('modal-lg', rendered)
        self.assertNotIn('modal-xl', rendered)
