import math
from typing import Any

from django import forms
from .models import Project, TestStep, TestCase, TestSuite, TestSuiteRun, TestCaseRun, TestStepRun


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'key'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'id': 'projectName'})
        self.fields['key'].widget.attrs.update({'class': 'form-control', 'id': 'projectKey', 'oninput': 'this.value = this.value.toUpperCase()', 'pattern': '\p{sc=Latin}*'})


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
        self.fields['name'].widget.attrs.update({'class': 'form-control me-2'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control me-2'})
        self.fields['description'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control h-100'})
        self.fields['preconditions'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control'})
        self.fields['postconditions'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control'})
        self.fields['parameters'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control h-100', 'id': 'testCaseParameters'})



class TestCaseFormset(forms.BaseModelFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if 'DELETE' in form.fields:
            form.fields['DELETE'].widget = forms.HiddenInput()



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
            action_size = math.ceil((len(item.action)/56) + (len(item.action)/200)) 
            expected_result_size = math.ceil((len(item.expected_result)/56) + (len(item.expected_result)/200))
            if action_size >= expected_result_size:
                self.fields['action'].widget.attrs.update({'rows': f'{action_size}'})
                self.fields['expected_result'].widget.attrs.update({'rows': f'{action_size}'})
            else:
                self.fields['action'].widget.attrs.update({'rows': f'{expected_result_size}'})
                self.fields['expected_result'].widget.attrs.update({'rows': f'{expected_result_size}'})
        else:
            self.fields['action'].widget.attrs.update({'rows': '1'})
            self.fields['expected_result'].widget.attrs.update({'rows': '1'})
        self.fields['action'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': ' list-group-item col'})
        self.fields['expected_result'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': ' list-group-item col'})



class TestSuiteForm(forms.ModelForm):
    class Meta:
        model = TestSuite
        fields = [
            'name',
            'description',
            'test_cases'
        ]


class TestStepRunFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(kwargs.get('queryset'), TestCase):
            self.queryset = TestStepRun.objects.none()
            self.initial = []
            teststeps = TestStep.objects.filter(test_case=kwargs.get('queryset'))
            self.extra = len(teststeps)
            for teststep in teststeps:
                self.initial.append({
                    'action': teststep.action,
                    'expected_result': teststep.expected_result
                })
        else:
            self.queryset = kwargs.get('queryset')
            self.extra = 0



class TestStepRunForm(forms.ModelForm):
    class Meta:
        model = TestStepRun
        fields = [
            'action',
            'expected_result',
            'result'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item = kwargs.get('initial')
        if item is not None:
            action_size = math.ceil((len(item['action'])/56) + (len(item['action'])/200)) 
            expected_result_size = math.ceil((len(item['expected_result'])/56) + (len(item['expected_result'])/200))
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
        