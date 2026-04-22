from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from django_sample_components.forms.registration_form import RegistrationForm


class PopupRegistrationFormComponentView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        return render(
            request,
            "django_sample_components/components/async_registration_form.html",
            {"form": RegistrationForm()},
        )
