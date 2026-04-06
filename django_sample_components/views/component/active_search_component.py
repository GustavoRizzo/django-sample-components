from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

DEMO_CONTACTS = [
    {"first_name": "Alice", "last_name": "Johnson", "email": "alice.johnson@example.com"},
    {"first_name": "Bob", "last_name": "Smith", "email": "bob.smith@example.com"},
    {"first_name": "Carol", "last_name": "Williams", "email": "carol.williams@example.com"},
    {"first_name": "David", "last_name": "Brown", "email": "david.brown@example.com"},
    {"first_name": "Eve", "last_name": "Davis", "email": "eve.davis@example.com"},
    {"first_name": "Frank", "last_name": "Miller", "email": "frank.miller@example.com"},
    {"first_name": "Grace", "last_name": "Wilson", "email": "grace.wilson@example.com"},
    {"first_name": "Henry", "last_name": "Moore", "email": "henry.moore@example.com"},
    {"first_name": "Iris", "last_name": "Taylor", "email": "iris.taylor@example.com"},
    {"first_name": "Jack", "last_name": "Anderson", "email": "jack.anderson@example.com"},
    {"first_name": "Karen", "last_name": "Thomas", "email": "karen.thomas@example.com"},
    {"first_name": "Leo", "last_name": "Jackson", "email": "leo.jackson@example.com"},
    {"first_name": "Mia", "last_name": "White", "email": "mia.white@example.com"},
    {"first_name": "Nathan", "last_name": "Harris", "email": "nathan.harris@example.com"},
    {"first_name": "Olivia", "last_name": "Martin", "email": "olivia.martin@example.com"},
    {"first_name": "Paul", "last_name": "Garcia", "email": "paul.garcia@example.com"},
    {"first_name": "Quinn", "last_name": "Martinez", "email": "quinn.martinez@example.com"},
    {"first_name": "Rachel", "last_name": "Robinson", "email": "rachel.robinson@example.com"},
    {"first_name": "Sam", "last_name": "Clark", "email": "sam.clark@example.com"},
    {"first_name": "Tina", "last_name": "Lewis", "email": "tina.lewis@example.com"},
]


class ActiveSearchComponent(View):
    def get(self, request):
        if not request.htmx:
            return HttpResponseBadRequest()

        query = request.GET.get("search", "").strip().lower()

        if not query:
            contacts = DEMO_CONTACTS
        else:
            contacts = [
                c for c in DEMO_CONTACTS
                if query in c["first_name"].lower()
                or query in c["last_name"].lower()
                or query in c["email"].lower()
            ]

        return render(
            request,
            "django_sample_components/partials/async_active_search_results.html",
            {"contacts": contacts},
        )
