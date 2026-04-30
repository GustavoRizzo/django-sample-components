from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from django_sample_components.views.component.counter_component import CounterComponentView


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
        context = {
            'counter_url': CounterComponentView.get_url(initial_value=0, step=1),
            'lazy_popup_url': reverse('django_sample_components:lazy_popup_component'),
        }
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


class ToastPage(View):
    def get(self, request):
        messages.success(request, "This is a success message!")
        messages.warning(request, "This is a warning message!")
        messages.error(request, "This is an error message!")
        messages.info(request, "This is an info message!")
        return render(request, 'django_sample_components/pages/toast.html')


class HtmxLoaderPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/htmx_loader.html')


class PopupRegistrationFormPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/popup_registration_form.html')


class DynamicContentButtonPage(View):
    def get(self, request):
        context = {
            'script_url': reverse('django_sample_components:dynamic_content_button_script'),
            'modal_url': reverse('django_sample_components:dynamic_content_button_modal'),
        }
        return render(request, 'django_sample_components/pages/dynamic_content_button.html', context)


class LazyLoadPage(View):
    def get(self, request):
        return render(request, 'django_sample_components/pages/lazy_load.html')
