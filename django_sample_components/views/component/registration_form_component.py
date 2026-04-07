from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from django_sample_components.forms.registration_form import SUBJECT_CAPACITY, TAKEN_USERNAMES, RegistrationForm


class RegistrationFormComponent(View):
    template_name = "django_sample_components/components/async_registration_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegistrationForm()})

    def post(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return render(request, self.template_name, {"form": form, "success": True})
        return render(request, self.template_name, {"form": form})


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
