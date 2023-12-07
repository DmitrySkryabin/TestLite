from django import forms
from .models import Test, TestPlan, TestPostcondition, TestPrecondition, TestStep


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = [
            'name',
            'description',
            'priority'
        ]



class TestPreconditionForm(forms.ModelForm):
    '''Форма с предусловиями теста'''
    class Meta:
        model = TestPrecondition
        fields = [
            'action',
            'expected_result',
            'position'
        ]



class TestPostconditionForm(forms.ModelForm):
    '''Форма с постусловиями теста'''
    class Meta:
        model = TestPostcondition
        fields = [
            'action',
            'expected_result',
            'position'
        ]



class TestStepForm(forms.ModelForm):
    '''Форма с шагами теста'''
    class Meta:
        model = TestStep
        fields = [
            'action',
            'expected_result',
            'position'
        ]



class TestPlanForm(forms.ModelForm):
    '''Форма для создания тест плана'''
    class Meta:
        model = TestPlan
        fields = [
            'name',
            'tests'
        ]