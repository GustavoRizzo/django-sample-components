from django.urls import include, path

from ..views import (
    ActiveSearchComponentView,
    ActiveSearchPage,
    CounterComponentView,
    CounterPage,
    HtmxLoaderPage,
    LazyLoadExternalComponentView,
    LazyLoadPage,
    LazyPopupComponentView,
    LazyPopupPage,
)

urlpatterns = [
    path('active-search/', ActiveSearchPage.as_view(), name='active_search'),
    path('htmx-loader/', HtmxLoaderPage.as_view(), name='htmx_loader'),
    path('active-search/component/', ActiveSearchComponentView.as_view(), name='active_search_component'),
    path('counter/', CounterPage.as_view(), name='counter'),
    path('counter/component/', CounterComponentView.as_view(), name='counter_component'),
    path('dynamic-forms/', include('django_sample_components.urls.dynamic_forms_urls')),
    path('lazy-load/', LazyLoadPage.as_view(), name='lazy_load'),
    path('lazy-load/external/', LazyLoadExternalComponentView.as_view(), name='lazy_load_external'),
    path('lazy-popup/', LazyPopupPage.as_view(), name='lazy_popup'),
    path('lazy-popup/component/', LazyPopupComponentView.as_view(), name='lazy_popup_component'),
]
