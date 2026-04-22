import json

from django.test import SimpleTestCase
from django.urls import reverse

from django_sample_components.utils import (
    VALID_TOAST_TYPES,
    get_json_show_toast,
    get_json_show_toasts,
)


class GetJsonShowToastTests(SimpleTestCase):
    def test_returns_show_toast_key(self):
        result = get_json_show_toast("Saved!", "success")
        self.assertIn('showToast', result)
        self.assertEqual(result['showToast']['message'], 'Saved!')
        self.assertEqual(result['showToast']['type'], 'success')

    def test_default_type_is_info(self):
        result = get_json_show_toast("Hello")
        self.assertEqual(result['showToast']['type'], 'info')

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            get_json_show_toast("Hello", "invalid")

    def test_all_valid_types_accepted(self):
        for t in VALID_TOAST_TYPES:
            result = get_json_show_toast("msg", t)
            self.assertEqual(result['showToast']['type'], t)


class GetJsonShowToastsTests(SimpleTestCase):
    def test_returns_show_toasts_key(self):
        result = get_json_show_toasts([{"message": "A", "type": "success"}])
        self.assertIn('showToasts', result)
        self.assertIsInstance(result['showToasts'], list)

    def test_multiple_items_preserved(self):
        items = [{"message": "A", "type": "success"}, {"message": "B", "type": "error"}]
        result = get_json_show_toasts(items)
        self.assertEqual(len(result['showToasts']), 2)
        self.assertEqual(result['showToasts'][0]['message'], 'A')
        self.assertEqual(result['showToasts'][1]['message'], 'B')

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            get_json_show_toasts([{"message": "A", "type": "invalid"}])

    def test_serializes_to_valid_json(self):
        result = get_json_show_toasts([{"message": "A", "type": "success"}, {"message": "B", "type": "warning"}])
        serialized = json.dumps(result)
        parsed = json.loads(serialized)
        self.assertEqual(len(parsed['showToasts']), 2)


class ToastDemoComponentViewTests(SimpleTestCase):
    url = reverse('django_sample_components:toast_demo_component')

    def test_get_without_htmx_returns_400(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_get_with_htmx_returns_200(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)

    def test_get_sets_hx_trigger_header(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertIn('HX-Trigger', response)

    def test_hx_trigger_contains_show_toasts(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        trigger = json.loads(response['HX-Trigger'])
        self.assertIn('showToasts', trigger)

    def test_show_toasts_has_multiple_items(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        trigger = json.loads(response['HX-Trigger'])
        self.assertGreater(len(trigger['showToasts']), 1)

    def test_show_toasts_items_have_message_and_type(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        trigger = json.loads(response['HX-Trigger'])
        for item in trigger['showToasts']:
            self.assertIn('message', item)
            self.assertIn('type', item)
            self.assertIn(item['type'], VALID_TOAST_TYPES)
