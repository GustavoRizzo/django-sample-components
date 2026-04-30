import json
from typing import Any

from django.contrib import messages
from django.forms import BaseForm, ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.generic.edit import FormView

from django_sample_components.utils import convert_django_messages_to_hx_triggers


class BaseFormComponentView(FormView):
    """Base HTMX form component. Enforces HX-Request, queues Django messages as toast
    notifications via HX-Trigger, and exposes get_success_context / get_error_context
    hooks for subclasses to customise the response context. Override get_success_message
    or get_error_message with a no-op to suppress the toast entirely."""

    success_message: str = "Operation completed successfully!"
    error_message: str = "Please fix the errors in the form."

    def get_success_message(self) -> None:
        messages.success(self.request, self.success_message)

    def get_error_message(self) -> None:
        messages.error(self.request, self.error_message)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.htmx:
            return HttpResponseBadRequest()
        return super().post(request, *args, **kwargs)

    def get_success_context(self, form: BaseForm) -> dict[str, Any]:
        ctx = self.get_context_data(form=form)
        ctx['form_valid'] = True
        return ctx

    def get_error_context(self, form: BaseForm) -> dict[str, Any]:
        ctx = self.get_context_data(form=form)
        ctx['form_invalid'] = True
        return ctx

    def _set_hx_trigger(self, response: HttpResponse) -> HttpResponse:
        trigger = convert_django_messages_to_hx_triggers(self.request)
        if trigger:
            response["HX-Trigger"] = json.dumps(trigger)
        return response

    def form_valid(self, form: BaseForm) -> HttpResponse:
        self.get_success_message()
        ctx = self.get_success_context(form)
        return self._set_hx_trigger(self.render_to_response(ctx))

    def form_invalid(self, form: BaseForm) -> HttpResponse:
        self.get_error_message()
        ctx = self.get_error_context(form)
        return self._set_hx_trigger(self.render_to_response(ctx))


class BaseCreateFormComponentView(BaseFormComponentView):
    """Extends BaseFormComponentView for forms that persist a model instance.
    Calls form.save() on success and makes the created object available as
    'object' in the success context."""

    def form_valid(self, form: ModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)

    def get_success_context(self, form: ModelForm) -> dict[str, Any]:
        ctx = super().get_success_context(form)
        ctx['object'] = self.object
        return ctx
