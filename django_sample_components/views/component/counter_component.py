import uuid

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View


class CounterComponent(View):
    template_name = 'django_sample_components/components/async_counter.html'

    @staticmethod
    def get_url(
        initial_value: int = 0,
        step: int = 1,
        min_value: int | None = None,
        max_value: int | None = None,
    ) -> str:
        """Returns the component URL with the given initial parameters as query string."""
        params = {'initial_value': initial_value, 'step': step}
        if min_value is not None:
            params['min_value'] = min_value
        if max_value is not None:
            params['max_value'] = max_value
        return f"{reverse('django_sample_components:counter_component')}?{urlencode(params)}"

    @staticmethod
    def _parse_optional_int(raw_value):
        if raw_value in (None, '', 'None'):
            return None
        try:
            return int(raw_value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _with_default(value, default):
        return default if value is None else value

    def _render_counter_component(self, request, *, id_counter, initial_value, step, min_value, max_value):
        context = {
            'id_counter': id_counter,
            'initial_value': initial_value,
            'step': step,
            'min_value': min_value,
            'max_value': max_value,
        }
        return render(request, self.template_name, context)

    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        initial_value = self._parse_optional_int(request.GET.get('initial_value'))
        step = self._parse_optional_int(request.GET.get('step'))
        min_value = self._parse_optional_int(request.GET.get('min_value'))
        max_value = self._parse_optional_int(request.GET.get('max_value'))

        return self._render_counter_component(
            request,
            id_counter=f'async-counter-{uuid.uuid4()}',
            initial_value=self._with_default(initial_value, 0),
            step=self._with_default(step, 1),
            min_value=min_value,
            max_value=max_value,
        )

    def post(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        current = self._with_default(self._parse_optional_int(request.POST.get('current_value')), 0)
        action = request.POST.get('action', 'add')
        step = self._with_default(self._parse_optional_int(request.POST.get('step')), 1)
        min_value = self._parse_optional_int(request.POST.get('min_value'))
        max_value = self._parse_optional_int(request.POST.get('max_value'))

        new_value = current + (step if action == 'add' else -step)

        if min_value is not None:
            new_value = max(new_value, min_value)
        if max_value is not None:
            new_value = min(new_value, max_value)

        id_counter = request.POST.get('id_counter') or f'async-counter-{uuid.uuid4()}'

        return self._render_counter_component(
            request,
            id_counter=id_counter,
            initial_value=new_value,
            step=step,
            min_value=min_value,
            max_value=max_value,
        )
