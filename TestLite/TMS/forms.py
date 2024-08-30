import math

from django import forms
from .models import TestStep, TestCase, TestSuite, TestSuiteRun, TestCaseRun, TestStepRun


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
        self.fields['action'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)'})
        self.fields['expected_result'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)'})



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
        