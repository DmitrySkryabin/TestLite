import math
from typing import Any

from django import forms
from django.forms.renderers import BaseRenderer
from django.utils.safestring import SafeText
from .models import Project, TestStep, TestCase, TestCaseFolder, TestSuite, TestSuiteRun, TestCaseRun, TestStepRun, AutotestSetting, AutotestSettingParam


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
        self.fields['key'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'projectKey', 
            'pattern': '\p{sc=Latin}*',
            'onchange': 'checkProjectKeyToExistName(this)'
            })

    

class TableModelMultipleChoiceField(forms.CheckboxSelectMultiple):
    template_name = "TMS/widgets/table_multiple_choice.html"

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        def add_selected_attr(testcase):
            # Добавялем новый атрибут, если у нас выбран данный тест кейс
            setattr(testcase, 'selected', True)
            return testcase
        
        if args[1] is None:
            context['testcases'] = [item[0].instance for item in self.choices]
        else:
            context['testcases'] = [item[0].instance if item[0].instance.id not in args[1] else add_selected_attr(item[0].instance) for item in self.choices]
        
        return context



class TestCaseFolderForm(forms.ModelForm):
    class Meta:
        model = TestCaseFolder
        fields = [
            'name',
            'test_cases'
        ]

    def __init__(self, project, *args, **kwargs):
        self.queryset = TestCaseFolder.objects.filter(project=project)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'id': 'folderName'})
        self.fields['test_cases'] = forms.ModelMultipleChoiceField(
            queryset=TestCase.objects.filter(project=project, archived=False),
            widget=TableModelMultipleChoiceField,
            required=False
        )



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
        self.fields['name'].widget.attrs.update({'class': 'form-control me-2', 'placeholder': 'Название тест кейса'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control me-2'})
        self.fields['description'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control h-100'})
        self.fields['preconditions'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control'})
        self.fields['postconditions'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control'})
        self.fields['parameters'].widget.attrs.update({'onkeyup': 'textAreaAdjust(this)', 'class': 'form-control h-100', 'id': 'testCaseParameters'})



class TestCaseFormset(forms.BaseModelFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if 'DELETE' in form.fields:
            form.fields['DELETE'].widget.attrs.update({'class': 'hide'})



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

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if project is None:
            queryset = TestCase.objects.filter(project=kwargs.get('instance').project)
        else:
            queryset = TestCase.objects.filter(project=Project.objects.get(key=project))
        
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['test_cases'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=TableModelMultipleChoiceField,
            required=True
        )



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



class AutotestSettingForm(forms.ModelForm):
    class Meta:
        model = AutotestSetting
        fields = [
            'url'
        ]
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['url'].widget.attrs.update({'class': 'form-control'})




class AutotestSettingParamForm(forms.ModelForm):
    class Meta:
        model = AutotestSettingParam
        fields = [
            'name',
            'value'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].widget.attrs.update({'class': 'form-control'})
            