from django.urls import include, path

from ..views import (
    ActiveSearchComponentView,
    CounterComponentView,
    LazyLoadComponentView,
    LazyLoadExternalComponentView,
    LazyPopupComponentView,
)

urlpatterns = [
    path('active-search/component/', ActiveSearchComponentView.as_view(), name='active_search_component'),
    path('counter/component/', CounterComponentView.as_view(), name='counter_component'),
    path('dynamic-forms/', include('django_sample_components.urls.dynamic_forms_urls')),
    path('lazy-load/', LazyLoadComponentView.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternalComponentView.as_view(), name='lazy_load_external'),
    path('lazy-popup/component/', LazyPopupComponentView.as_view(), name='lazy_popup_component'),
]
