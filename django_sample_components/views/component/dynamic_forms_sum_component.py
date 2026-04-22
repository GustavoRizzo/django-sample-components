import json

from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.views.generic.edit import FormView

from django_sample_components.forms.sum_form import SumForm
from django_sample_components.utils import convert_django_messages_to_hx_triggers


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

    def _set_hx_trigger(self, response):
        trigger = convert_django_messages_to_hx_triggers(self.request)
        if trigger:
            response["HX-Trigger"] = json.dumps(trigger)
        return response

    def form_valid(self, form):
        messages.success(self.request, "Result calculated successfully!")
        return self._set_hx_trigger(self.render_to_response(self.get_context_data(form=form, result=form.get_result())))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
