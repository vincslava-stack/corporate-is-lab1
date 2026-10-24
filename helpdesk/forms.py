
from django import forms
from django.contrib.auth import get_user_model

from .models import Category, Ticket


User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "author",
            "category",
            "priority",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Кратко опишите проблему"}
            ),
            "author": forms.TextInput(
                attrs={"placeholder": "ФИО заявителя"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Подробно опишите проблему",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 5:
            raise forms.ValidationError(
                "Тема заявки должна содержать минимум 5 символов."
            )

        return title

    def clean_author(self):
        author = self.cleaned_data["author"].strip()

        if not author:
            raise forms.ValidationError(
                "Укажите, кто обратился с заявкой."
            )

        return author


class TicketProcessForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status", "assignee"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        it_group_users = User.objects.filter(
            groups__name="ИТ-отдел"
        ).distinct()

        self.fields["assignee"].queryset = it_group_users
        self.fields["assignee"].required = False
        self.fields["assignee"].label = "Ответственный сотрудник"
        self.fields["status"].label = "Статус заявки"
