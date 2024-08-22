from django import forms
from .models import TestStep



class TestStepForm(forms.ModelForm):
    '''Форма с шагами теста'''
    class Meta:
        model = TestStep
        fields = [
            'action',
            'expected_result',
            'position'
        ]