from django.urls import path

from .views import Counter

urlpatterns = [
    path('counter/', Counter.as_view(), name='counter'),
]
