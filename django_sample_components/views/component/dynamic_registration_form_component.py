import json

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from django_sample_components.forms.registration_form import SUBJECT_CAPACITY, TAKEN_USERNAMES, RegistrationForm


class RegistrationFormComponentView(FormView):
    template_name = "django_sample_components/components/async_registration_form.html"
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponseBadRequest()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = self.render_to_response(self.get_context_data(form=form, success=True))
        response["HX-Trigger"] = json.dumps(
            {
                "showToast": {
                    "message": "Registration submitted successfully!",
                    "type": "success",
                }
            }
        )
        return response

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response["HX-Trigger"] = json.dumps(
            {
                "showToast": {
                    "message": "Please fix the errors in the form.",
                    "type": "error",
                }
            }
        )
        return response


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
