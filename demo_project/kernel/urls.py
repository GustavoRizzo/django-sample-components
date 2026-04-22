from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from django_sample_components import urls as component_urls

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Demo pages
    path('', views.HomePage.as_view(), name='home'),
    path('greeting/', views.GreetingPage.as_view(), name='greeting'),
    path('alert/', views.AlertPage.as_view(), name='alert'),
    path('typewriter/', views.TypewriterPage.as_view(), name='typewriter'),
    path('button/', views.ButtonPage.as_view(), name='button'),
    path('popup/', views.PopupPage.as_view(), name='popup'),
    path('toast/', views.ToastPage.as_view(), name='toast'),
    path('async/counter/', views.CounterPage.as_view(), name='counter'),
    path('async/active-search/', views.ActiveSearchPage.as_view(), name='active_search'),
    path('async/htmx-loader/', views.HtmxLoaderPage.as_view(), name='htmx_loader'),
    path('async/lazy-load/page/', views.LazyLoadPage.as_view(), name='lazy_load_page'),
    path('async/lazy-popup/', views.LazyPopupPage.as_view(), name='lazy_popup'),
    path('async/dynamic-forms/sum/', views.DynamicFormsSumPage.as_view(), name='dynamic_forms_sum'),
    path('async/dynamic-forms/registration/', views.RegistrationFormPage.as_view(), name='registration_form'),
    path('async/popup-registration/', views.PopupRegistrationFormPage.as_view(), name='popup_registration_form'),
    # Library component endpoints
    path('', include(component_urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
