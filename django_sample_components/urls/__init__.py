from django.urls import include, path

app_name = 'django_sample_components'

urlpatterns = [
    path('async/', include('django_sample_components.urls.async_urls')),
]
