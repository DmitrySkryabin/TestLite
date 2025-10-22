from django.db import models

from .validators import TestCaseInnerValidator


class TestCase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    inner_content = models.JSONField(default=list, validators=[TestCaseInnerValidator()])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title