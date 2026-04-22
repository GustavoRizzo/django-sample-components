import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

from django_sample_components.utils import convert_django_messages_to_hx_triggers


class ToastDemoComponentView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()
        messages.success(request, 'Operation completed successfully!')
        messages.info(request, 'Here is some useful information.')
        messages.error(request, 'Something went wrong on the server.')
        trigger = convert_django_messages_to_hx_triggers(request)
        response = HttpResponse()
        if trigger:
            response['HX-Trigger'] = json.dumps(trigger)
        return response
