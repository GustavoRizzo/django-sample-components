import re
import time
import uuid
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View


class Home(View):
    def get(self, request):
        context = {
            'url_pypi': settings.URL_PYPI,
            'url_github': settings.URL_GITHUB,
        }
        return render(request, 'django_sample_components/pages/home.html', context)


class Greeting(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/greeting.html')


class Alert(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/alert.html')


class Typewriter(View):
    def get(self, request):
        words = [
            "Hello, World!",
            "Welcome to Django Sample Components.",
            "Enjoy the typewriter effect!",
            "Customize it with your own words.",
        ]
        return render(request, 'django_sample_components/pages/typewriter.html', {"words": words})


class Button(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/button.html')


class Popup(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/popup.html')


class CounterPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/counter.html')


class CounterComponent(View):
    template_name = 'django_sample_components/components/async_counter.html'

    @staticmethod
    def _parse_optional_int(raw_value):
        if raw_value in (None, '', 'None'):
            return None
        try:
            return int(raw_value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _with_default(value, default):
        return default if value is None else value

    def _render_counter_component(self, request, *, id_counter, initial_value, step, min_value, max_value):
        context = {
            'id_counter': id_counter,
            'initial_value': initial_value,
            'step': step,
            'min_value': min_value,
            'max_value': max_value,
        }
        return render(request, self.template_name, context)

    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        initial_value = self._parse_optional_int(request.GET.get('initial_value'))
        step = self._parse_optional_int(request.GET.get('step'))
        min_value = self._parse_optional_int(request.GET.get('min_value'))
        max_value = self._parse_optional_int(request.GET.get('max_value'))

        return self._render_counter_component(
            request,
            id_counter=f"async-counter-{uuid.uuid4()}",
            initial_value=self._with_default(initial_value, 0),
            step=self._with_default(step, 1),
            min_value=min_value,
            max_value=max_value,
        )

    def post(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        current = self._with_default(self._parse_optional_int(request.POST.get('current_value')), 0)
        action = request.POST.get('action', 'add')
        step = self._with_default(self._parse_optional_int(request.POST.get('step')), 1)
        min_value = self._parse_optional_int(request.POST.get('min_value'))
        max_value = self._parse_optional_int(request.POST.get('max_value'))

        new_value = current + (step if action == 'add' else -step)

        if min_value is not None:
            new_value = max(new_value, min_value)
        if max_value is not None:
            new_value = min(new_value, max_value)

        id_counter = request.POST.get('id_counter') or f"async-counter-{uuid.uuid4()}"

        return self._render_counter_component(
            request,
            id_counter=id_counter,
            initial_value=new_value,
            step=step,
            min_value=min_value,
            max_value=max_value,
        )


class LazyLoad(View):
    def get(self, request):
        if not request.htmx:
            return render(request, 'django_sample_components/pages/lazy_load.html')

        raw_delay_ms = request.GET.get('delay_ms')
        try:
            delay_ms = int(raw_delay_ms) if raw_delay_ms not in (None, '') else 0
        except ValueError:
            delay_ms = 0

        # Clamp delay to keep demo responses predictable and avoid excessive waits.
        delay_ms = max(0, min(delay_ms, 10000))
        if delay_ms > 0:
            time.sleep(delay_ms / 1000)

        context = {'loaded_at': timezone.now()}
        return render(request, 'django_sample_components/partials/async_lazy_load_content.html', context)


class LazyLoadExternal(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        target_url = request.GET.get('target_url', '').strip()
        parsed_url = urlparse(target_url)
        if not target_url or parsed_url.scheme not in {'http', 'https'}:
            return HttpResponseBadRequest()

        raw_delay_ms = request.GET.get('delay_ms')
        try:
            delay_ms = int(raw_delay_ms) if raw_delay_ms not in (None, '') else 0
        except ValueError:
            delay_ms = 0

        delay_ms = max(0, min(delay_ms, 10000))
        if delay_ms > 0:
            time.sleep(delay_ms / 1000)

        context = {
            'target_url': target_url,
            'title': None,
            'error': None,
        }

        try:
            request_obj = Request(target_url, headers={'User-Agent': 'django-sample-components/1.0'})
            with urlopen(request_obj, timeout=8) as response:
                body = response.read(120000).decode('utf-8', errors='replace')

            title_match = re.search(r'<title[^>]*>(.*?)</title>', body, flags=re.IGNORECASE | re.DOTALL)
            if title_match:
                context['title'] = re.sub(r'\s+', ' ', title_match.group(1)).strip()
        except (ValueError, OSError, URLError):
            context['error'] = 'Unable to fetch external content from the provided URL.'

        return render(request, 'django_sample_components/partials/async_lazy_load_external_content.html', context)
