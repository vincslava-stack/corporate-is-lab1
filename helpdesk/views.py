

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketForm, TicketProcessForm
from .models import Ticket


def hello(request):
    return HttpResponse("Привет! Это учёт заявок ИТ-отдела.")


def visible_tickets(user):
    tickets = Ticket.objects.select_related(
        "category", "created_by", "assignee"
    )

    if user.has_perm("helpdesk.change_ticket"):
        return tickets

    return tickets.filter(created_by=user)


@login_required
def ticket_list(request):
    tickets = visible_tickets(request.user).order_by("-created_at")

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")

    if query:
        tickets = tickets.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(description__icontains=query)
        )

    if status:
        tickets = tickets.filter(status=status)

    return render(
        request,
        "helpdesk/ticket_list.html",
        {
            "tickets": tickets,
            "query": query,
            "selected_status": status,
        },
    )


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(
        visible_tickets(request.user),
        pk=pk,
    )

    process_form = None
    if request.user.has_perm("helpdesk.change_ticket"):
        process_form = TicketProcessForm(instance=ticket)

    return render(
        request,
        "helpdesk/ticket_detail.html",
        {
            "ticket": ticket,
            "process_form": process_form,
            "can_edit_ticket": ticket.can_be_edited_by(request.user),
        },
    )


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Заявка успешно создана.")
            return redirect(ticket)
    else:
        form = TicketForm()

    return render(
        request,
        "helpdesk/ticket_form.html",
        {"form": form, "title": "Создание заявки"},
    )


@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(
        visible_tickets(request.user),
        pk=pk,
    )

    if not ticket.can_be_edited_by(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка обновлена.")
            return redirect(ticket)
    else:
        form = TicketForm(instance=ticket)

    return render(
        request,
        "helpdesk/ticket_form.html",
        {"form": form, "title": "Редактирование заявки"},
    )


@login_required
@permission_required("helpdesk.change_ticket", raise_exception=True)
def ticket_process(request, pk):
    if request.method != "POST":
        return redirect("ticket_detail", pk=pk)

    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketProcessForm(request.POST, instance=ticket)

    if form.is_valid():
        form.save()
        messages.success(request, "Статус заявки обновлён.")
    else:
        messages.error(request, "Не удалось обработать заявку.")

    return redirect(ticket)
