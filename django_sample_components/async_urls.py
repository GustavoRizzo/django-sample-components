from django.urls import path

from .views import Counter, CounterAPI

urlpatterns = [
    path('counter/', Counter.as_view(), name='counter'),
    path('partial/counter/', CounterAPI.as_view(), name='counter_partial'),
]
