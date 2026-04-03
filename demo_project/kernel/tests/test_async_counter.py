from django.template import Template, Context
from django.test import SimpleTestCase
from django.urls import reverse


class AsyncCounterTemplateTagTests(SimpleTestCase):
    """Test the async_counter template tag rendering."""

    def test_renders_with_defaults(self):
        template = Template("{% load async_tags %}{% async_counter %}")
        rendered = template.render(Context())

        self.assertIn('async-counter-', rendered)
        self.assertIn('hx-post', rendered)
        self.assertIn('counter-display', rendered)

    def test_renders_initial_value(self):
        template = Template("{% load async_tags %}{% async_counter initial_value=42 %}")
        rendered = template.render(Context())

        self.assertIn('42', rendered)

    def test_renders_step_in_hx_vals(self):
        template = Template("{% load async_tags %}{% async_counter initial_value=0 step=5 %}")
        rendered = template.render(Context())

        self.assertIn('"step": 5', rendered)

    def test_renders_min_max_in_hx_vals(self):
        """min_value and max_value must appear in hx-vals so the API can enforce them."""
        template = Template("{% load async_tags %}{% async_counter initial_value=5 min_value=0 max_value=10 %}")
        rendered = template.render(Context())

        self.assertIn('"min_value": "0"', rendered)
        self.assertIn('"max_value": "10"', rendered)

    def test_renders_without_min_max(self):
        """When min/max are not set, hx-vals still renders (with empty strings)."""
        template = Template("{% load async_tags %}{% async_counter initial_value=0 %}")
        rendered = template.render(Context())

        self.assertIn('hx-vals', rendered)
        self.assertIn('"min_value"', rendered)
        self.assertIn('"max_value"', rendered)


class AsyncCounterPageTests(SimpleTestCase):
    """Test the counter demo page."""

    url = reverse('django_sample_components:counter')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b'htmx.org', response.content)

    def test_page_contains_component(self):
        response = self.client.get(self.url)
        self.assertIn(b'async-counter-', response.content)

    def test_page_contains_csrf_listener(self):
        """Page must set X-CSRFToken on HTMX requests."""
        response = self.client.get(self.url)
        self.assertIn(b'htmx:configRequest', response.content)
        self.assertIn(b'X-CSRFToken', response.content)


class AsyncCounterAPITests(SimpleTestCase):
    """Test the counter API endpoint (/api/counter/)."""

    url = reverse('django_sample_components:counter_api')

    def _post(self, **kwargs):
        return self.client.post(self.url, kwargs)

    # --- Basic operations ---

    def test_increment(self):
        response = self._post(action='add', current_value='0', step='1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1', response.content)

    def test_decrement(self):
        response = self._post(action='subtract', current_value='5', step='1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'4', response.content)

    def test_custom_step(self):
        response = self._post(action='add', current_value='0', step='5')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'5', response.content)

    def test_goes_negative_without_min(self):
        response = self._post(action='subtract', current_value='0', step='5')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'-5', response.content)

    # --- Sequential operations (regression: was always sending initial_value) ---

    def test_sequential_increments(self):
        """Each call must receive the updated value from the previous response."""
        value = '0'
        for expected in range(1, 4):
            response = self._post(action='add', current_value=value, step='1')
            self.assertEqual(response.status_code, 200)
            value = str(expected)
            self.assertIn(value.encode(), response.content)

    def test_sequential_decrements(self):
        value = '3'
        for expected in range(2, -1, -1):
            response = self._post(action='subtract', current_value=value, step='1')
            self.assertEqual(response.status_code, 200)
            value = str(expected)
            self.assertIn(value.encode(), response.content)

    # --- Min/max enforcement (regression: limits were not applied) ---

    def test_does_not_exceed_max(self):
        response = self._post(action='add', current_value='10', step='1', min_value='', max_value='10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'10', response.content)

    def test_does_not_go_below_min(self):
        response = self._post(action='subtract', current_value='0', step='1', min_value='0', max_value='')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0', response.content)

    def test_clamps_to_max_when_step_exceeds_boundary(self):
        response = self._post(action='add', current_value='8', step='5', min_value='', max_value='10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'10', response.content)

    def test_clamps_to_min_when_step_exceeds_boundary(self):
        response = self._post(action='subtract', current_value='2', step='5', min_value='0', max_value='')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0', response.content)

    def test_limits_not_applied_when_absent(self):
        """Without min/max the counter must go beyond those values freely."""
        response = self._post(action='add', current_value='100', step='1', min_value='', max_value='')
        self.assertIn(b'101', response.content)

        response = self._post(action='subtract', current_value='-10', step='1', min_value='', max_value='')
        self.assertIn(b'-11', response.content)
