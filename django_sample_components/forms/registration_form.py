from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Submit
from django import forms
from django.urls import reverse_lazy

TAKEN_USERNAMES = {"alice", "bob", "carol", "david", "eve", "admin"}

SUBJECT_CHOICES = [
    ("", "--- Select a subject ---"),
    ("math", "Mathematics"),
    ("physics", "Physics"),
    ("history", "History"),
    ("art", "Art"),
    ("music", "Music"),
]

SUBJECT_CAPACITY = {
    "math": {"enrolled": 28, "max": 30},
    "physics": {"enrolled": 30, "max": 30},
    "history": {"enrolled": 15, "max": 30},
    "art": {"enrolled": 29, "max": 30},
    "music": {"enrolled": 5, "max": 30},
}


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        min_length=1,
        widget=forms.TextInput(attrs={
            "hx-get": reverse_lazy("django_sample_components:registration_check_username"),
            "hx-trigger": "keyup changed delay:400ms",
            "hx-target": "#username-feedback",
            "hx-swap": "innerHTML",
        }),
    )
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            "hx-get": reverse_lazy("django_sample_components:registration_check_subject"),
            "hx-trigger": "change",
            "hx-target": "#subject-feedback",
            "hx-swap": "innerHTML",
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_of_birth"].widget.attrs["max"] = date.today().isoformat()
        self.helper = FormHelper()
        self.helper.form_id = "registration-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("django_sample_components:registration_form_component"),
            "hx-target": "#registration-form-wrapper",
            "hx-swap": "outerHTML",
        }
        self.helper.layout = Layout(
            Field("username"),
            HTML('<div id="username-feedback" class="form-text mb-2"></div>'),
            Field("password"),
            Field("date_of_birth"),
            Field("subject"),
            HTML('<div id="subject-feedback" class="form-text mb-2"></div>'),
            Submit("submit", "Register", css_class="btn btn-primary mt-2"),
        )

    def clean_username(self):
        value = self.cleaned_data.get("username", "")
        if value.lower() in TAKEN_USERNAMES:
            raise forms.ValidationError("That username is already taken.")
        return value

    def clean_subject(self):
        value = self.cleaned_data.get("subject", "")
        cap = SUBJECT_CAPACITY.get(value)
        if cap and cap["enrolled"] >= cap["max"]:
            raise forms.ValidationError("This subject has reached its enrollment limit.")
        return value

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob and dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob
