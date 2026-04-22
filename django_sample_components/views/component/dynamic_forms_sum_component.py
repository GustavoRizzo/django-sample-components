from django_sample_components.forms.sum_form import SumForm
from django_sample_components.views.component.base import BaseFormComponentView


class DynamicFormsSumComponentView(BaseFormComponentView):
    template_name = "django_sample_components/components/async_sum_form.html"
    form_class = SumForm
    success_message = "Result calculated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("result", None)
        return context

    def get_success_context(self, form):
        return self.get_context_data(form=form, result=form.get_result())
