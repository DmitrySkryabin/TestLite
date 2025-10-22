from django.contrib import admin
from django import forms

from .models import TestCase
from .widgets.admin.testcase_step import TestCaseStepsWidget


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = "__all__"
        widgets = {
            # Применяем кастомный виджет к полю inner_content
            "inner_content": TestCaseStepsWidget()
        }


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    form = TestCaseForm
    list_display = ("id", "title", "created_at", "updated_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")