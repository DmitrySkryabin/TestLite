from django import forms
from .models import TestRun, ResultChoice


# class TestRunForm(forms.Form):

#     result = forms.CharField(label='Результат')
#     type = forms.CharField(label='Тип')

class TestRunForm(forms.ModelForm):
    class Meta:
        model = TestRun
        fields = [
            'result',
            'type'
        ]



class SelectResultForm(forms.ModelForm):
    '''Форма для выполнения сохранения результатов теста
    Изменяемая часть это результат, останые данные о шагах записаны в переменные'''
    def __init__(self, *args, **kwargs):
        if kwargs['instance'] is not None:
            self.action = kwargs['instance'].action # получем и записываем поле action из запроса который вызывает форму из modelformset_factorys
            self.expected_result = kwargs['instance'].expected_result # 
        super().__init__(*args, **kwargs)

    class Meta:
        fields = [
            'result'
        ]
