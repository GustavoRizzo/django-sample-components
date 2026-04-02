from django.urls import path

from .views import Alert, Button, Greeting, Home, Popup, Typewriter

app_name = 'django_sample_components'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('greeting/', Greeting.as_view(), name='greeting'),
    path('alert/', Alert.as_view(), name='alert'),
    path('typewriter/', Typewriter.as_view(), name='typewriter'),
    path('button/', Button.as_view(), name='button'),
    path('popup/', Popup.as_view(), name='popup'),
]
