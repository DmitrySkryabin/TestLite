from django import forms
from .models import TestRun, ResultChoice



class TestRunForm(forms.ModelForm):
    class Meta:
        model = TestRun
        fields = [
            'result',
            'type'
        ]



class SelectResultForm(forms.Form):
    '''Форма для выполнения сохранения результатов теста
    Изменяемая часть это результат, останые данные о шагах записаны в переменные'''
    action = forms.CharField(widget=forms.HiddenInput())
    expected_result = forms.CharField(widget=forms.HiddenInput())
    result = forms.ChoiceField(choices=[('', '---------')] + ResultChoice.choices, required=False)

    def __init__(self, result_required:bool=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if result_required:
            self.fields['result'].required = True


TestResultsFormset = forms.formset_factory(SelectResultForm, extra=0)

