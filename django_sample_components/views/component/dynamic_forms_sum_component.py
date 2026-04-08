import json

from django.http import HttpRequest, HttpResponseBadRequest
from django.forms import Form
from django.shortcuts import render
from django.views import View

from django_sample_components.forms.sum_form import SumForm


class DynamicFormsSumComponentView(View):
    template_name = "django_sample_components/components/async_sum_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": SumForm(), "result": None})

    def post(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        form = SumForm(request.POST)
        response = render(request, self.template_name, {"form": form, "result": form.get_result()})
        response = self.trigger_toast_message(response, form)
        return response

    def trigger_toast_message(self, response: HttpRequest, form: Form) -> HttpRequest:
        if form.is_valid():
            response["HX-Trigger"] = json.dumps(
                {
                    "showToast": {
                        "message": "Result calculated successfully!",
                        "type": "success",
                    }
                }
            )
        return response
