import re
import time
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


class LazyLoadExternalComponentView(View):
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
