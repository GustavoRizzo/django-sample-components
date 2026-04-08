import time

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View


class LazyLoadComponentView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

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
