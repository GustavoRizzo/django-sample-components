import json

from django.http import HttpResponseBadRequest
from django.views.generic.edit import FormView

from django_sample_components.forms.sum_form import SumForm


class DynamicFormsSumComponentView(FormView):
    template_name = "django_sample_components/components/async_sum_form.html"
    form_class = SumForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("result", None)
        return context

    def post(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponseBadRequest()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = self.render_to_response(self.get_context_data(form=form, result=form.get_result()))
        response["HX-Trigger"] = json.dumps(
            {
                "showToast": {
                    "message": "Result calculated successfully!",
                    "type": "success",
                }
            }
        )
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
