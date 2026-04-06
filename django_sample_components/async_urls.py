from django.urls import path

from .views import Counter, LazyLoad, LazyLoadExternal

urlpatterns = [
    path('counter/', Counter.as_view(), name='counter'),
    path('lazy-load/', LazyLoad.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternal.as_view(), name='lazy_load_external'),
]
