import math

from django import forms
from .models import TestStep, TestCase


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = [
            'name',
            'description',
            'preconditions',
            'postconditions',
            'priority',
            'parameters',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item:TestCase = kwargs.get('instance')
        self.fields['description'].widget.attrs.update({'rows': f'{math.ceil(len(item.description)/124)}', 'onkeyup': 'textAreaAdjust(this)'})
        self.fields['preconditions'].widget.attrs.update({'rows': f'{math.ceil(len(item.preconditions)/50)}', 'onkeyup': 'textAreaAdjust(this)'})
        self.fields['postconditions'].widget.attrs.update({'rows': f'{math.ceil(len(item.postconditions)/50)}', 'onkeyup': 'textAreaAdjust(this)'})
        self.fields['parameters'].widget.attrs.update({'rows': f'{math.ceil(len(item.parameters)/50)}', 'onkeyup': 'textAreaAdjust(this)'})



class TestStepForm(forms.ModelForm):
    '''Форма с шагами теста'''
    class Meta:
        model = TestStep
        fields = [
            'action',
            'expected_result',
            'position'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item:TestStep = kwargs.get('instance')
        if item is not None:
            action_size = math.ceil(len(item.action)/56)
            expected_result_size = math.ceil(len(item.expected_result)/56)
            if action_size >= expected_result_size:
                self.fields['action'].widget.attrs.update({'rows': f'{action_size}'})
                self.fields['expected_result'].widget.attrs.update({'rows': f'{action_size}'})
            else:
                self.fields['action'].widget.attrs.update({'rows': f'{expected_result_size}'})
                self.fields['expected_result'].widget.attrs.update({'rows': f'{expected_result_size}'})
        else:
            self.fields['action'].widget.attrs.update({'rows': '1'})
            self.fields['expected_result'].widget.attrs.update({'rows': '1'})
        self.fields['action'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)'})
        self.fields['expected_result'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)'})