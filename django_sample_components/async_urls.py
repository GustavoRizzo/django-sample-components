from django.urls import path

from .views import (
    ActiveSearchComponent,
    ActiveSearchPage,
    CheckSubjectPartialView,
    CheckUsernamePartialView,
    CounterComponent,
    CounterPage,
    DynamicFormsSumComponent,
    DynamicFormsSumPage,
    LazyLoadExternalComponent,
    LazyLoadPage,
    LazyPopupComponent,
    LazyPopupPage,
    RegistrationFormComponent,
    RegistrationFormPage,
)

urlpatterns = [
    path('active-search/', ActiveSearchPage.as_view(), name='active_search'),
    path('active-search/component/', ActiveSearchComponent.as_view(), name='active_search_component'),
    path('counter/', CounterPage.as_view(), name='counter'),
    path('counter/component/', CounterComponent.as_view(), name='counter_component'),
    path('dynamic-forms/sum/', DynamicFormsSumPage.as_view(), name='dynamic_forms_sum'),
    path('dynamic-forms/sum/component/', DynamicFormsSumComponent.as_view(), name='dynamic_forms_sum_component'),
    path('dynamic-forms/registration/', RegistrationFormPage.as_view(), name='registration_form'),
    path('dynamic-forms/registration/component/', RegistrationFormComponent.as_view(),
         name='registration_form_component'),
    path('dynamic-forms/registration/check-username/', CheckUsernamePartialView.as_view(),
         name='registration_check_username'),
    path('dynamic-forms/registration/check-subject/', CheckSubjectPartialView.as_view(),
         name='registration_check_subject'),
    path('lazy-load/', LazyLoadPage.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternalComponent.as_view(), name='lazy_load_external'),
    path('lazy-popup/', LazyPopupPage.as_view(), name='lazy_popup'),
    path('lazy-popup/component/', LazyPopupComponent.as_view(), name='lazy_popup_component'),
]
