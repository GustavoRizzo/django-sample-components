from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.urls import reverse_lazy


class SumForm(forms.Form):
    number_a = forms.FloatField(label="Number A")
    number_b = forms.FloatField(label="Number B")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "sum-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("django_sample_components:dynamic_forms_sum_component"),
            "hx-target": "#sum-form-component-wrapper",
            "hx-swap": "outerHTML",
        }
        self.helper.layout = Layout(
            Row(
                Column("number_a", css_class="col-md-6"),
                Column("number_b", css_class="col-md-6"),
            ),
            Submit("submit", "Result", css_class="btn btn-primary mt-2"),
        )

    def get_result(self):
        if self.is_valid():
            return self.cleaned_data["number_a"] + self.cleaned_data["number_b"]
        return None
