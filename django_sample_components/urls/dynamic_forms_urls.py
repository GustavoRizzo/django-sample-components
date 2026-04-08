from django.urls import path

from ..views import (
    CheckSubjectPartialView,
    CheckUsernamePartialView,
    DynamicFormsSumComponentView,
    RegistrationFormComponentView,
)

urlpatterns = [
    path('sum/component/', DynamicFormsSumComponentView.as_view(), name='dynamic_forms_sum_component'),
    path('registration/component/', RegistrationFormComponentView.as_view(), name='registration_form_component'),
    path('registration/check-username/', CheckUsernamePartialView.as_view(), name='registration_check_username'),
    path('registration/check-subject/', CheckSubjectPartialView.as_view(), name='registration_check_subject'),
]
