from django.urls import path

from .views import CounterComponent, CounterPage, LazyLoadExternalComponent, LazyLoadPage

urlpatterns = [
    path('counter/', CounterPage.as_view(), name='counter'),
    path('counter/component/', CounterComponent.as_view(), name='counter_component'),
    path('lazy-load/', LazyLoadPage.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternalComponent.as_view(), name='lazy_load_external'),
]
