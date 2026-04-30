from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


class DynamicContentButtonScriptResponseView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        script = "<script>alert('Hello from the server! The button fetched this script and it ran immediately.');</script>"
        return HttpResponse(script)


class DynamicContentButtonModalResponseView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        return render(
            request,
            "django_sample_components/partials/dynamic_content_button_modal_response.html",
        )
