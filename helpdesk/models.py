
from django.db import models


class Ticket(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Выполнена"

    title = models.CharField("Тема", max_length=200)
    author = models.CharField("Кто обратился", max_length=100)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    def __str__(self):
        return self.title
