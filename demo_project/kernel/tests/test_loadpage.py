from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    """Test class to verify the home page is accessible."""
    app_name = 'django_sample_components'

    home_page_url = reverse(f"{app_name}:home")
    greeting_page_url = reverse(f"{app_name}:greeting")
    alert_page_url = reverse(f"{app_name}:alert")

    def test_home_page_status_code(self):
        response = self.client.get(self.home_page_url)
        self.assertEqual(response.status_code, 200)

    def test_greeting_page_status_code(self):
        response = self.client.get(self.greeting_page_url)
        self.assertEqual(response.status_code, 200)

    def test_alert_page_status_code(self):
        response = self.client.get(self.alert_page_url)
        self.assertEqual(response.status_code, 200)
