
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Category, Ticket


User = get_user_model()


class TicketModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test-password-123",
        )
        self.category = Category.objects.create(
            name="Программное обеспечение",
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            title="Не работает программа",
            author="Иван Иванов",
            category=self.category,
            created_by=self.user,
        )
        self.assertEqual(ticket.status, Ticket.Status.NEW)
        self.assertEqual(ticket.priority, Ticket.Priority.NORMAL)
        self.assertEqual(ticket.created_by, self.user)

    def test_ticket_string_representation(self):
        ticket = Ticket.objects.create(
            title="Проблема с компьютером",
            author="Иван Иванов",
            created_by=self.user,
        )
        self.assertEqual(str(ticket), "Проблема с компьютером")


class TicketViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test-password-123",
        )
        self.ticket = Ticket.objects.create(
            title="Не работает принтер",
            author="Иван Иванов",
            description="Принтер не печатает.",
            created_by=self.user,
        )

    def test_ticket_list_requires_login(self):
        response = self.client.get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_sees_own_ticket(self):
        self.client.login(
            username="test_user",
            password="test-password-123",
        )
        response = self.client.get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не работает принтер")


    def test_user_can_create_ticket(self):
        self.client.login(
            username="test_user",
            password="test-password-123",
        )
        response = self.client.post(
            reverse("ticket_create"),
            {
                "title": "Не работает клавиатура",
                "author": "Пётр Петров",
                "category": "",
                "priority": "normal",
                "description": "Клавиатура не реагирует.",
            },
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get(title="Не работает клавиатура")
        self.assertEqual(ticket.created_by, self.user)
        self.assertEqual(response.url, reverse(
            "ticket_detail",
            kwargs={"pk": ticket.pk},
        ))

    def test_user_cannot_edit_completed_ticket(self):
        self.ticket.status = Ticket.Status.DONE
        self.ticket.save()

        self.client.login(
            username="test_user",
            password="test-password-123",
        )
        response = self.client.get(
            reverse("ticket_update", kwargs={"pk": self.ticket.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_it_employee_can_process_ticket(self):
        group = Group.objects.create(name="ИТ-отдел")
        user = User.objects.create_user(
            username="it_support",
            password="test-password-123",
        )
        user.groups.add(group)

        permission = Permission.objects.get(
            content_type__app_label="helpdesk",
            codename="change_ticket",
        )
        user.user_permissions.add(permission)

        self.client.login(
            username="it_support",
            password="test-password-123",
        )
        response = self.client.post(
            reverse("ticket_process", kwargs={"pk": self.ticket.pk}),
            {
                "status": Ticket.Status.IN_PROGRESS,
                "assignee": "",
            },
        )
        self.assertRedirects(
            response,
            reverse("ticket_detail", kwargs={"pk": self.ticket.pk}),
        )
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.IN_PROGRESS)
