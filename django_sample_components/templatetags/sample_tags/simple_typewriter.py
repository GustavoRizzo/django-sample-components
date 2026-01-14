import json

from django.template.loader import render_to_string


def simple_typewriter(words: str = None):
    if words is None:
        words = ['Please provide', 'a list', 'of words', 'to display']
    return render_to_string('django_sample_components/components/simple_typewriter.html', {"words": json.dumps(words)})
