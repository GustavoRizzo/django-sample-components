from django.urls import include, path

from ..views import AlertPage, ButtonPage, GreetingPage, HomePage, PopupPage, ToastPage, TypewriterPage

app_name = 'django_sample_components'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('greeting/', GreetingPage.as_view(), name='greeting'),
    path('alert/', AlertPage.as_view(), name='alert'),
    path('typewriter/', TypewriterPage.as_view(), name='typewriter'),
    path('button/', ButtonPage.as_view(), name='button'),
    path('popup/', PopupPage.as_view(), name='popup'),
    path('toast/', ToastPage.as_view(), name='toast'),
    path('async/', include('django_sample_components.urls.async_urls')),
]
