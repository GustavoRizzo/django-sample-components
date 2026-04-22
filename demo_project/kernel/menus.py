from django.urls import reverse_lazy
from simple_menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Home", reverse_lazy("home"), weight=10, exact_url=True))

Menu.add_item("main", MenuItem("Static", "#", weight=20, children=[
    MenuItem("Greeting", reverse_lazy("greeting"), weight=10),
    MenuItem("Alert", reverse_lazy("alert"), weight=20),
    MenuItem("Typewriter", reverse_lazy("typewriter"), weight=30),
    MenuItem("Button", reverse_lazy("button"), weight=40),
    MenuItem("Popup", reverse_lazy("popup"), weight=50),
    MenuItem("Toast", reverse_lazy("toast"), weight=60),
]))

Menu.add_item("main", MenuItem("Async", "#", weight=30, children=[
    MenuItem("Counter", reverse_lazy("counter"), weight=10),
    MenuItem("Lazy Load", reverse_lazy("lazy_load_page"), weight=20),
    MenuItem("Active Search", reverse_lazy("active_search"), weight=30),
    MenuItem("Lazy Popup", reverse_lazy("lazy_popup"), weight=40),
    MenuItem("HTMX Loader", reverse_lazy("htmx_loader"), weight=50),
]))

Menu.add_item("main", MenuItem("Dynamic Forms", "#", weight=40, children=[
    MenuItem("Sum Form", reverse_lazy("dynamic_forms_sum"), weight=10),
    MenuItem("Registration Form", reverse_lazy("registration_form"), weight=20),
    MenuItem("Popup Registration Form", reverse_lazy("popup_registration_form"), weight=30),
]))
