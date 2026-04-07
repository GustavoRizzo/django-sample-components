import time

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views import View


class HomePage(View):
    def get(self, request):
        context = {
            'url_pypi': settings.URL_PYPI,
            'url_github': settings.URL_GITHUB,
        }
        return render(request, 'django_sample_components/pages/home.html', context)


class GreetingPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/greeting.html')


class AlertPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/alert.html')


class TypewriterPage(View):
    def get(self, request):
        words = [
            "Hello, World!",
            "Welcome to Django Sample Components.",
            "Enjoy the typewriter effect!",
            "Customize it with your own words.",
        ]
        return render(request, 'django_sample_components/pages/typewriter.html', {'words': words})


class ButtonPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/button.html')


class PopupPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/popup.html')


class CounterPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/counter.html')


class LazyPopupPage(View):
    def get(self, request):
        from .component.counter_component import CounterComponent
        context = {'counter_url': CounterComponent.get_url(initial_value=0, step=1)}
        return render(request, 'django_sample_components/pages/lazy_popup.html', context)


class ActiveSearchPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/active_search.html')


class DynamicFormsSumPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/dynamic_forms_sum.html')


class RegistrationFormPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/dynamic_forms_registration.html')


class LazyLoadPage(View):
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
