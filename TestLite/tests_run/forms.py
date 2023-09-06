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


class SelectResultForm(forms.Form):
    result = forms.ChoiceField(choices=[('', '---------')] + ResultChoice.choices)

    # def set_name(self, id):
    #     self.fields['result'].widget.attrs.update({
    #         'name': id
    #     })
    #     return self