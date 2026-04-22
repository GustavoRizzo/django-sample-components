import json

from django.contrib.messages import get_messages

VALID_TOAST_TYPES = {'success', 'error', 'danger', 'warning', 'info', 'primary', 'secondary'}

_DJANGO_TAG_TO_TOAST_TYPE: dict[str, str] = {
    'debug': 'info',
    'info': 'info',
    'success': 'success',
    'warning': 'warning',
    'error': 'error',
}


def get_json_show_toast(message: str, toast_type: str = 'info') -> dict:
    """Returns an HX-Trigger payload dict to show a single toast notification.

    Usage in a view:
        import json
        response["HX-Trigger"] = json.dumps(get_json_show_toast("Saved!", "success"))
    """
    if toast_type not in VALID_TOAST_TYPES:
        raise ValueError(f"Invalid toast type '{toast_type}'. Accepted values: {', '.join(sorted(VALID_TOAST_TYPES))}")
    return {"showToast": {"message": message, "type": toast_type}}


def get_json_show_toasts(items: list[dict]) -> dict:
    """Returns an HX-Trigger payload dict to show multiple toast notifications at once.

    Uses "showToasts" (plural) with an array payload to avoid duplicate JSON key collisions —
    Python dicts silently discard duplicate keys, so {"showToast": A, "showToast": B} would
    only keep B after json.dumps.

    Usage in a view:
        import json
        response["HX-Trigger"] = json.dumps(get_json_show_toasts([
            {"message": "Saved!", "type": "success"},
            {"message": "Check the warnings.", "type": "warning"},
        ]))
    """
    for item in items:
        if item.get("type") not in VALID_TOAST_TYPES:
            raise ValueError(
                f"Invalid toast type '{item.get('type')}'. Accepted values: {', '.join(sorted(VALID_TOAST_TYPES))}"
            )
    return {"showToasts": items}


def convert_django_messages_to_hx_triggers(request) -> dict:
    """Consumes all queued Django messages and returns an HX-Trigger payload dict.

    Returns:
        {}                                              — no queued messages
        {"showToast": {"message": ..., "type": ...}}    — exactly one message
        {"showToasts": [...]}                           — two or more messages

    Note: calling this consumes the messages — they will NOT appear on the next page load.

    Usage in a view:
        trigger = convert_django_messages_to_hx_triggers(request)
        response = render(...)
        if trigger:
            response["HX-Trigger"] = json.dumps(trigger)
    """
    msgs = list(get_messages(request))
    if not msgs:
        return {}
    if len(msgs) == 1:
        msg = msgs[0]
        return get_json_show_toast(str(msg), _DJANGO_TAG_TO_TOAST_TYPE.get(msg.tags, 'info'))
    items = [
        {"message": str(msg), "type": _DJANGO_TAG_TO_TOAST_TYPE.get(msg.tags, 'info')}
        for msg in msgs
    ]
    return get_json_show_toasts(items)
