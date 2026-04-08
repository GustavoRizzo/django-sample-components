from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


class AsyncSumFormTemplateTagTests(SimpleTestCase):
    """Test the async_sum_form template tag rendering."""

    def _render(self):
        return Template("{% load async_tags %}{% async_sum_form %}").render(Context())

    def test_renders_component_wrapper(self):
        self.assertIn('sum-form-component-wrapper', self._render())

    def test_renders_form_fields(self):
        rendered = self._render()
        self.assertIn('number_a', rendered)
        self.assertIn('number_b', rendered)

    def test_renders_htmx_post_attribute(self):
        rendered = self._render()
        self.assertIn('hx-post', rendered)
        self.assertIn('hx-swap="outerHTML"', rendered)
        self.assertIn('hx-target="#sum-form-component-wrapper"', rendered)

    def test_renders_submit_button(self):
        self.assertIn('Result', self._render())

    def test_no_result_on_initial_render(self):
        self.assertNotIn('sum-result', self._render())


class DynamicFormsSumPageTests(SimpleTestCase):
    """Test the dynamic forms sum demo page."""

    url = reverse('dynamic_forms_sum')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b'htmx.min.js', response.content)

    def test_page_contains_component(self):
        response = self.client.get(self.url)
        self.assertIn(b'sum-form-component-wrapper', response.content)

    def test_page_contains_csrf_header(self):
        response = self.client.get(self.url)
        self.assertIn(b'hx-headers', response.content)
        self.assertIn(b'X-CSRFToken', response.content)


class DynamicFormsSumComponentTests(SimpleTestCase):
    """Test the sum form component endpoint (/async/dynamic-forms/sum/component/)."""

    url = reverse('django_sample_components:dynamic_forms_sum_component')

    def _post(self, **kwargs):
        return self.client.post(self.url, kwargs, HTTP_HX_REQUEST='true')

    def test_get_renders_component(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sum-form-component-wrapper', response.content)
        self.assertNotIn(b'sum-result', response.content)

    def test_post_without_htmx_returns_400(self):
        response = self.client.post(self.url, {'number_a': '3', 'number_b': '5'})
        self.assertEqual(response.status_code, 400)

    def test_valid_sum_of_integers(self):
        response = self._post(number_a='3', number_b='5')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'8', response.content)
        self.assertIn(b'sum-result', response.content)

    def test_valid_sum_of_floats(self):
        response = self._post(number_a='1.5', number_b='2.5')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'4.0', response.content)

    def test_valid_sum_with_negative_numbers(self):
        response = self._post(number_a='-3', number_b='10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'7', response.content)

    def test_invalid_post_shows_form_errors(self):
        response = self._post(number_a='not-a-number', number_b='5')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'sum-result', response.content)
        self.assertIn(b'number_a', response.content)

    def test_empty_post_shows_form_errors(self):
        response = self._post()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'sum-result', response.content)
