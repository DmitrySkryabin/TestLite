from dataclasses import dataclass 
from django.shortcuts import redirect
from django.urls import reverse
from django.forms import modelformset_factory
from .models import TestPrecondition, TestPlan, TestStep, TestPostcondition
from .forms import TestPreconditionForm, TestStepForm, TestPostconditionForm, TestPlanForm


class TestCreateUpdateMixin:
    '''
    Миксин для создания/редактирования теста и его атрибутов
    Сюда вынесен общий для создания и редактирования код
    '''
    @dataclass
    class Formsets:
        form_precondition_formset: object
        form_step_formset: object
        form_postcondition_formset: object 


    def _set_formsets(self):
        '''Заполняем формсеты для начального отображения'''
        self._formsets = self.Formsets(
            form_precondition_formset = self.form_precondition_formset(queryset=TestPrecondition.objects.none(), prefix='preconditions'),
            form_step_formset = self.form_step_formset(queryset=TestStep.objects.none(), prefix='steps'),
            form_postcondition_formset = self.form_postcondition_formset(queryset=TestPostcondition.objects.none(), prefix='postconditions')
        )


    def get_context_data(self, **kwargs):
        '''Получаем необходимые данные для отправки на темплейт'''
        context = super().get_context_data(**kwargs)
        self.form_precondition_formset = modelformset_factory(form=TestPreconditionForm, model=TestPrecondition)
        self.form_step_formset = modelformset_factory(form=TestStepForm, model=TestStep)
        self.form_postcondition_formset = modelformset_factory(form=TestPostconditionForm, model=TestPostcondition)

        if self.request.POST:
            context['form_precondition_formset'] = self.form_precondition_formset(self.request.POST, prefix='preconditions')
            context['form_step_formset'] = self.form_step_formset(self.request.POST, prefix='steps')
            context['form_postcondition_formset'] = self.form_postcondition_formset(self.request.POST, prefix='postconditions')
        else:
            self._set_formsets() # полуаем формсеты
            context['form_precondition_formset'] = self._formsets.form_precondition_formset
            context['form_step_formset'] = self._formsets.form_step_formset
            context['form_postcondition_formset'] = self._formsets.form_postcondition_formset

        return context


    def form_valid(self, form):
        '''Сохранение формы и валидация формсетов'''
        context = self.get_context_data()
        if context['form_precondition_formset'].is_valid() and context['form_step_formset'].is_valid() and context['form_postcondition_formset'].is_valid():
            test = form.save(commit=False)
            test.author = self.request.user
            test.save()
            for instance in context['form_precondition_formset'].save(commit=False):
                instance.test = test
                instance.save()
            for instance in context['form_step_formset'].save(commit=False):
                instance.test = test
                instance.save()
            for instance in context['form_postcondition_formset'].save(commit=False):
                instance.test = test
                instance.save()
            return redirect(reverse('tests:test_detail', kwargs={'id': test.id}))
        else:
            return self.render_to_response(self.get_context_data(form=form))
        


class TestPlanCreateUpdateMixin:
    '''Общий миксин для создания и редактирования тест плана'''
    model = TestPlan
    form_class = TestPlanForm

    def get_success_url(self):
        return reverse('tests:test_plan_detail', kwargs={'test_plan_id': self.object.id})
    


class TestPlanGetObjectMixin:
    '''Миксин дл яполучения обьчект тест плана'''
    def get_object(self):
        test_plan = TestPlan.objects.get(id=self.kwargs.get('test_plan_id'))
        return test_plan