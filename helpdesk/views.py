
from django.http import HttpResponse
from django.shortcuts import render

from .models import Ticket


def hello(request):
    return HttpResponse("Привет! Это учёт заявок ИТ-отдела.")


def ticket_list(request):
    tickets = Ticket.objects.order_by("-created_at")
    return render(
        request,
        "helpdesk/ticket_list.html",
        {"tickets": tickets},
    )
