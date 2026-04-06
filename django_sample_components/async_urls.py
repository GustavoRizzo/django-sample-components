from django.urls import path

from .views import (
    ActiveSearchComponent,
    ActiveSearchPage,
    CounterComponent,
    CounterPage,
    LazyLoadExternalComponent,
    LazyLoadPage,
    LazyPopupComponent,
    LazyPopupPage,
)

urlpatterns = [
    path('active-search/', ActiveSearchPage.as_view(), name='active_search'),
    path('active-search/component/', ActiveSearchComponent.as_view(), name='active_search_component'),
    path('counter/', CounterPage.as_view(), name='counter'),
    path('counter/component/', CounterComponent.as_view(), name='counter_component'),
    path('lazy-load/', LazyLoadPage.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternalComponent.as_view(), name='lazy_load_external'),
    path('lazy-popup/', LazyPopupPage.as_view(), name='lazy_popup'),
    path('lazy-popup/component/', LazyPopupComponent.as_view(), name='lazy_popup_component'),
]
