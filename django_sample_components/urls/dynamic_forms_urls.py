from django.urls import path

from ..views import (
    CheckSubjectPartialView,
    CheckUsernamePartialView,
    DynamicFormsSumComponentView,
    DynamicFormsSumPage,
    RegistrationFormComponentView,
    RegistrationFormPage,
)

urlpatterns = [
    path('sum/', DynamicFormsSumPage.as_view(), name='dynamic_forms_sum'),
    path('sum/component/', DynamicFormsSumComponentView.as_view(), name='dynamic_forms_sum_component'),
    path('registration/', RegistrationFormPage.as_view(), name='registration_form'),
    path('registration/component/', RegistrationFormComponentView.as_view(), name='registration_form_component'),
    path('registration/check-username/', CheckUsernamePartialView.as_view(), name='registration_check_username'),
    path('registration/check-subject/', CheckSubjectPartialView.as_view(), name='registration_check_subject'),
]
