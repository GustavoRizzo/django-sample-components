from django.template import Context, Template
from django.test import SimpleTestCase


class SimpleAlertTemplateTagTests(SimpleTestCase):
    """Test the simple_alert template tag rendering."""

    def test_renders_close_button_by_default(self):
        template = Template('{% load sample_tags %}{% simple_alert %}content{% endsimple_alert %}')
        rendered = template.render(Context())

        self.assertIn('btn-close', rendered)

    def test_does_not_render_close_button_when_disabled(self):
        template = Template('{% load sample_tags %}{% simple_alert close_button=False %}content{% endsimple_alert %}')
        rendered = template.render(Context())

        self.assertNotIn('btn-close', rendered)
