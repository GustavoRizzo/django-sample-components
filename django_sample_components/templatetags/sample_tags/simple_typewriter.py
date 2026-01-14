from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def simple_typewriter():
    return render_to_string('django_sample_components/components/simple_typewriter.html', {})
