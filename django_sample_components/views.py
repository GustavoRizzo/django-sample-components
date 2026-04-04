from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseBadRequest
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
