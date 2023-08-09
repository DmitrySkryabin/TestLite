from TestLite.utils import query_debugger
from .models import Test, TestPostcondition, TestPrecondition, TestStep
from django.forms import modelformset_factory
from django.forms.models import BaseModelForm
from django.db.models.query import QuerySet
from .forms import TestStepForm, TestPostconditionForm, TestPreconditionForm


class Return:
    '''Класс для возврата элементов в view'''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)



class TestServices():
    '''Сервисы для обработки данных тестов'''
    @query_debugger
    def get_all_test_attributes(id) -> dict:
        '''Возвращает все что связано с конкретным тестом'''
        test = Test.objects.get(id=id)

        test_postconditions = TestPostcondition.objects.filter(test=test).all()
        test_preconditions = TestPrecondition.objects.filter(test=test).all()
        test_steps = TestStep.objects.filter(test=test).all()

        return Return(
            test = test,
            test_postconditions = test_postconditions,
            test_preconditions = test_preconditions,
            test_steps = test_steps
        )
    
    
    @query_debugger
    def get_all_tests():
        '''Возвращает список (QuerySet) всех тестов'''
        return Test.objects.all()


    def get_tests_all_forms(data: Return = None) -> dict:
        '''
        Возвращает все формы для редакирования теста и его шагов
        preconditions, steps, postconditions
        Получает: Return где хранятся queryset для этих моделей
        '''
        TestPreconditionFormset = modelformset_factory(model=TestPrecondition, form=TestPreconditionForm)       # Предусловия
        TestStepFormset = modelformset_factory(model=TestStep, form=TestStepForm)                               # Шаги
        TestPostconditionFormset = modelformset_factory(model=TestPostcondition, form=TestPostconditionForm)    # Постусловия

        if data is None:
            print('heh')
            data.test_preconditions = QuerySet()
            data.test_steps = QuerySet()
            data.test_postconditions = QuerySet()

        return Return(
            form_precondition_formset=TestPreconditionFormset(queryset=data.test_preconditions),
            form_step_formset=TestStepFormset(queryset=data.test_steps),
            form_postcondition_formset=TestPostconditionFormset(queryset=data.test_postconditions)
        ).__dict__
    

    def save_test(form: BaseModelForm, request) -> BaseModelForm:
        '''Сохранение экземпляра теста'''
        test = form.instance
        test.author = request.user
        test.save()

        return test