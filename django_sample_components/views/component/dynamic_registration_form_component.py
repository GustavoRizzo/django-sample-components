import json

from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from django_sample_components.forms.registration_form import SUBJECT_CAPACITY, TAKEN_USERNAMES, RegistrationForm
from django_sample_components.utils import convert_django_messages_to_hx_triggers


class RegistrationFormComponentView(FormView):
    template_name = "django_sample_components/components/async_registration_form.html"
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponseBadRequest()
        return super().post(request, *args, **kwargs)

    def _set_hx_trigger(self, response):
        trigger = convert_django_messages_to_hx_triggers(self.request)
        if trigger:
            response["HX-Trigger"] = json.dumps(trigger)
        return response

    def form_valid(self, form):
        messages.success(self.request, "Registration submitted successfully!")
        return self._set_hx_trigger(self.render_to_response(self.get_context_data(form=form, success=True)))

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors in the form.")
        return self._set_hx_trigger(self.render_to_response(self.get_context_data(form=form)))


class CheckUsernamePartialView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        username = request.GET.get("username", "").strip()
        context = {}
        if len(username) > 3:
            if username.lower() in TAKEN_USERNAMES:
                context = {"valid": False, "message": "That username is already taken."}
            else:
                context = {"valid": True, "message": "Username is available."}
        return render(request, "django_sample_components/partials/registration_username_check.html", context)


class CheckSubjectPartialView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        subject = request.GET.get("subject", "").strip()
        context = {}
        cap = SUBJECT_CAPACITY.get(subject)
        if cap:
            remaining = cap["max"] - cap["enrolled"]
            if remaining <= 0:
                context = {"valid": False, "message": "This subject is full — no spots available."}
            elif remaining <= 3:
                context = {"valid": True, "warn": True, "message": f"Only {remaining} spot(s) left!"}
            else:
                context = {"valid": True, "message": f"{remaining} spots available."}
        return render(request, "django_sample_components/partials/registration_subject_check.html", context)
