from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View


class LazyPopupComponentView(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        context = {"loaded_at": timezone.now()}
        return render(request, "django_sample_components/partials/async_lazy_popup_content.html", context)
