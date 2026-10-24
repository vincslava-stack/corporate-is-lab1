
from django.urls import path

from . import views

urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("tickets/", views.ticket_list, name="ticket_list"),
]
