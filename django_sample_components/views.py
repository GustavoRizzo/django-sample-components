import re
import time
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


class Counter(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/counter.html')

    def post(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        current = int(request.POST.get('current_value', 0))
        action = request.POST.get('action', 'add')
        step = int(request.POST.get('step', 1))
        raw_min = request.POST.get('min_value')
        raw_max = request.POST.get('max_value')
        min_value = int(raw_min) if raw_min not in (None, '', 'None') else None
        max_value = int(raw_max) if raw_max not in (None, '', 'None') else None

        new_value = current + (step if action == 'add' else -step)

        if min_value is not None:
            new_value = max(new_value, min_value)
        if max_value is not None:
            new_value = min(new_value, max_value)

        context = {'value': new_value}
        return render(request, 'django_sample_components/partials/async_counter_value.html', context)


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
