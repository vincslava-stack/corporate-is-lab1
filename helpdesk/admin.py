
from django.contrib import admin

from .models import Category, Ticket


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "priority",
        "status",
        "created_by",
        "assignee",
        "created_at",
    )
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "author", "description")
    list_select_related = ("category", "created_by", "assignee")
