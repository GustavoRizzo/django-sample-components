from django.template import Context, Template
from django.test import SimpleTestCase
from django.urls import reverse


class AsyncActiveSearchTemplateTagTests(SimpleTestCase):
    """Test the async_active_search template tag rendering."""

    def test_renders_with_defaults(self):
        template = Template("{% load async_tags %}{% async_active_search %}")
        rendered = template.render(Context())

        self.assertIn('async-active-search-', rendered)
        self.assertIn('hx-get', rendered)
        self.assertIn('type="search"', rendered)

    def test_renders_custom_placeholder(self):
        template = Template('{% load async_tags %}{% async_active_search placeholder="Find a contact..." %}')
        rendered = template.render(Context())

        self.assertIn('Find a contact...', rendered)

    def test_renders_search_url(self):
        template = Template('{% load async_tags %}{% async_active_search search_url="/custom/search/" %}')
        rendered = template.render(Context())

        self.assertIn('/custom/search/', rendered)

    def test_renders_results_tbody(self):
        template = Template("{% load async_tags %}{% async_active_search %}")
        rendered = template.render(Context())

        self.assertIn('-results', rendered)
        self.assertIn('<tbody', rendered)

    def test_renders_htmx_trigger(self):
        template = Template("{% load async_tags %}{% async_active_search %}")
        rendered = template.render(Context())

        self.assertIn('hx-trigger', rendered)
        self.assertIn('delay:300ms', rendered)


class ActiveSearchPageTests(SimpleTestCase):
    """Test the active-search demo page."""

    url = reverse('django_sample_components:active_search')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_contains_htmx(self):
        response = self.client.get(self.url)
        self.assertIn(b'htmx.min.js', response.content)

    def test_page_contains_component(self):
        response = self.client.get(self.url)
        self.assertIn(b'async-active-search-', response.content)

    def test_page_contains_csrf_header(self):
        response = self.client.get(self.url)
        self.assertIn(b'X-CSRFToken', response.content)


class ActiveSearchComponentTests(SimpleTestCase):
    """Test the active-search HTMX endpoint (/async/active-search/component/)."""

    url = reverse('django_sample_components:active_search_component')

    def _get(self, search="", **kwargs):
        return self.client.get(self.url, {"search": search}, HTTP_HX_REQUEST='true', **kwargs)

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_post_not_allowed(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 405)

    def test_empty_search_returns_all_contacts(self):
        response = self._get(search="")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice', response.content)
        self.assertIn(b'Tina', response.content)

    def test_search_by_first_name(self):
        response = self._get(search="alice")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice', response.content)
        self.assertNotIn(b'Bob', response.content)

    def test_search_by_last_name(self):
        response = self._get(search="smith")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smith', response.content)
        self.assertNotIn(b'Alice', response.content)

    def test_search_by_email(self):
        response = self._get(search="garcia")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'garcia', response.content)

    def test_search_case_insensitive(self):
        response = self._get(search="ALICE")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice', response.content)

    def test_no_match_returns_empty_state(self):
        response = self._get(search="zzznomatch")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No contacts found', response.content)
