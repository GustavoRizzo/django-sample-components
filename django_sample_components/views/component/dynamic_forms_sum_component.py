from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from django_sample_components.forms.sum_form import SumForm


class DynamicFormsSumComponent(View):
    template_name = "django_sample_components/components/async_sum_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": SumForm(), "result": None})

    def post(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        form = SumForm(request.POST)
        return render(request, self.template_name, {"form": form, "result": form.get_result()})
