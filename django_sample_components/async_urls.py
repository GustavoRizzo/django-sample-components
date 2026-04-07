from django.urls import path

from .views import (
    ActiveSearchComponentView,
    ActiveSearchPage,
    CheckSubjectPartialView,
    CheckUsernamePartialView,
    CounterComponentView,
    CounterPage,
    DynamicFormsSumComponentView,
    DynamicFormsSumPage,
    LazyLoadExternalComponentView,
    LazyLoadPage,
    LazyPopupComponentView,
    LazyPopupPage,
    RegistrationFormComponentView,
    RegistrationFormPage,
)

urlpatterns = [
    path('active-search/', ActiveSearchPage.as_view(), name='active_search'),
    path('active-search/component/', ActiveSearchComponentView.as_view(), name='active_search_component'),
    path('counter/', CounterPage.as_view(), name='counter'),
    path('counter/component/', CounterComponentView.as_view(), name='counter_component'),
    path('dynamic-forms/sum/', DynamicFormsSumPage.as_view(), name='dynamic_forms_sum'),
    path('dynamic-forms/sum/component/', DynamicFormsSumComponentView.as_view(), name='dynamic_forms_sum_component'),
    path('dynamic-forms/registration/', RegistrationFormPage.as_view(), name='registration_form'),
    path('dynamic-forms/registration/component/', RegistrationFormComponentView.as_view(),
         name='registration_form_component'),
    path('dynamic-forms/registration/check-username/', CheckUsernamePartialView.as_view(),
         name='registration_check_username'),
    path('dynamic-forms/registration/check-subject/', CheckSubjectPartialView.as_view(),
         name='registration_check_subject'),
    path('lazy-load/', LazyLoadPage.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternalComponentView.as_view(), name='lazy_load_external'),
    path('lazy-popup/', LazyPopupPage.as_view(), name='lazy_popup'),
    path('lazy-popup/component/', LazyPopupComponentView.as_view(), name='lazy_popup_component'),
]
