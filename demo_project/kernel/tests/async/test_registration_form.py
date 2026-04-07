from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


class AsyncRegistrationFormTemplateTagTests(SimpleTestCase):
    """Test the async_registration_form template tag rendering."""

    def _render(self):
        return Template("{% load async_tags %}{% async_registration_form %}").render(Context())

    def test_renders_component_wrapper(self):
        self.assertIn('registration-form-wrapper', self._render())

    def test_renders_username_field(self):
        self.assertIn('id_username', self._render())

    def test_renders_htmx_post_attribute(self):
        rendered = self._render()
        self.assertIn('hx-post', rendered)
        self.assertIn('hx-swap="outerHTML"', rendered)
        self.assertIn('hx-target="#registration-form-wrapper"', rendered)

    def test_renders_htmx_username_check(self):
        rendered = self._render()
        self.assertIn('check-username', rendered)

    def test_renders_htmx_subject_check(self):
        rendered = self._render()
        self.assertIn('check-subject', rendered)

    def test_no_success_on_initial_render(self):
        self.assertNotIn('Registration successful', self._render())


class RegistrationFormPageTests(SimpleTestCase):
    """Test the registration form demo page."""

    url = reverse('django_sample_components:registration_form')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b'htmx.min.js', response.content)

    def test_page_contains_component(self):
        response = self.client.get(self.url)
        self.assertIn(b'registration-form-wrapper', response.content)

    def test_page_contains_csrf_header(self):
        response = self.client.get(self.url)
        self.assertIn(b'hx-headers', response.content)
        self.assertIn(b'X-CSRFToken', response.content)


class RegistrationFormComponentTests(SimpleTestCase):
    """Test the registration form component endpoint."""

    url = reverse('django_sample_components:registration_form_component')

    def _post(self, **kwargs):
        return self.client.post(self.url, kwargs, HTTP_HX_REQUEST='true')

    def test_get_renders_component(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'registration-form-wrapper', response.content)
        self.assertNotIn(b'Registration successful', response.content)

    def test_post_without_htmx_returns_400(self):
        response = self.client.post(self.url, {'username': 'newuser', 'password': 'pass1234',
                                               'date_of_birth': '1990-01-01', 'subject': 'music'})
        self.assertEqual(response.status_code, 400)

    def test_valid_post_shows_success(self):
        response = self._post(username='newuser99', password='securepass1', date_of_birth='1995-06-15', subject='music')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.content)
        self.assertIn(b'newuser99', response.content)

    def test_invalid_post_taken_username(self):
        response = self._post(username='alice', password='securepass1', date_of_birth='1995-06-15', subject='music')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Registration successful', response.content)
        self.assertIn(b'registration-form-wrapper', response.content)

    def test_invalid_post_full_subject(self):
        response = self._post(
            username='newuser99', password='securepass1', date_of_birth='1995-06-15', subject='physics'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Registration successful', response.content)

    def test_invalid_post_future_dob(self):
        response = self._post(username='newuser99', password='securepass1', date_of_birth='2099-01-01', subject='music')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Registration successful', response.content)

    def test_invalid_post_empty_fields(self):
        response = self._post()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Registration successful', response.content)
        self.assertIn(b'registration-form-wrapper', response.content)


class CheckUsernamePartialTests(SimpleTestCase):
    """Test the username inline check endpoint."""

    url = reverse('django_sample_components:registration_check_username')

    def _get(self, username):
        return self.client.get(self.url, {'username': username}, HTTP_HX_REQUEST='true')

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url, {'username': 'alice'})
        self.assertEqual(response.status_code, 400)

    def test_short_username_returns_empty(self):
        response = self._get('ab')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.strip(), b'')

    def test_available_username(self):
        response = self._get('newuser999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'available', response.content)

    def test_taken_username(self):
        response = self._get('alice')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'taken', response.content)

    def test_case_insensitive_taken_check(self):
        response = self._get('ALICE')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'taken', response.content)


class CheckSubjectViewTests(SimpleTestCase):
    """Test the subject inline check endpoint."""

    url = reverse('django_sample_components:registration_check_subject')

    def _get(self, subject):
        return self.client.get(self.url, {'subject': subject}, HTTP_HX_REQUEST='true')

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url, {'subject': 'music'})
        self.assertEqual(response.status_code, 400)

    def test_full_subject(self):
        response = self._get('physics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'full', response.content)

    def test_available_subject(self):
        response = self._get('music')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'available', response.content)

    def test_near_full_subject(self):
        response = self._get('art')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'left', response.content)

    def test_empty_subject_returns_empty(self):
        response = self._get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.strip(), b'')
