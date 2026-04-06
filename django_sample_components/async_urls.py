from django.urls import path

from .views import CounterComponent, CounterPage, LazyLoad, LazyLoadExternal

urlpatterns = [
    path('counter/', CounterPage.as_view(), name='counter'),
    path('counter/component/', CounterComponent.as_view(), name='counter_component'),
    path('lazy-load/', LazyLoad.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternal.as_view(), name='lazy_load_external'),
]
