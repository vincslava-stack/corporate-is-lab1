
from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        NORMAL = "normal", "Обычный"
        HIGH = "high", "Высокий"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Выполнена"

    title = models.CharField("Тема", max_length=200)
    author = models.CharField("Кто обратился", max_length=100)
    description = models.TextField("Описание проблемы", blank=True)

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tickets",
    )

    priority = models.CharField(
        "Приоритет",
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Создал пользователь",
        on_delete=models.PROTECT,
        related_name="created_tickets",
        null=True,
        blank=True,
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Ответственный сотрудник",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ticket_detail", kwargs={"pk": self.pk})

    def can_be_edited_by(self, user):
        if not user.is_authenticated:
            return False

        if user.has_perm("helpdesk.change_ticket"):
            return True

        return self.created_by_id == user.pk and self.status == self.Status.NEW

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]
