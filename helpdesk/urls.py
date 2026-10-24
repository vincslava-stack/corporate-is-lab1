
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="ticket_list",
            permanent=False,
        ),
    ),
    path("hello/", views.hello, name="hello"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path(
        "tickets/<int:pk>/",
        views.ticket_detail,
        name="ticket_detail",
    ),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path(
        "tickets/<int:pk>/edit/",
        views.ticket_update,
        name="ticket_update",
    ),
    path(
        "tickets/<int:pk>/process/",
        views.ticket_process,
        name="ticket_process",
    ),
]
