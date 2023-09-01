from dataclasses import dataclass
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .services import TestServices
from .forms import TestForm, TestPostconditionForm, TestPreconditionForm, TestStepForm
from .models import Test, TestPrecondition, TestStep, TestPostcondition
from django.forms import modelformset_factory



class TestDetailView(DetailView):
    '''Отображение детальной информации по тесту'''
    context_object_name = 'data'
    template_name = 'tests/test_detail.html'

    def get_object(self):
        test_id = self.kwargs.get('id')
        data = TestServices.get_all_test_attributes(id=test_id)

        return data



class TestListView(ListView):
    '''Список всех тестов'''
    queryset = TestServices.get_all_tests()



class TestCreateUpdateMixin:
    '''
    Миксин для создания/редактирования теста и его атрибутов
    Сюда вынесен общий для обоих код
    '''
    @dataclass
    class Formsets:
        form_precondition_formset: object
        form_step_formset: object
        form_postcondition_formset: object 


    def _set_formsets(self):
        '''Инициализируем формсеты'''
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



class TestCreateView(TestCreateUpdateMixin ,CreateView):
    '''Создание теста и его атрибутов'''
    model=Test
    form_class=TestForm



class TestUpdateView(TestCreateUpdateMixin, UpdateView):
    '''Редактирование теста и его атрибутов'''
    model = Test
    form_class = TestForm


    def _set_formsets(self):
        '''
        Переопределяем логику отображения формсетов атрибутов класса
        чтобы при редактировании были указаны уже имеющиеся данные
        '''
        self._formsets = self.Formsets(
                form_precondition_formset = self.form_precondition_formset(queryset=TestPrecondition.objects.filter(test__id=self.kwargs.get('id')), prefix='preconditions'),
                form_step_formset = self.form_step_formset(queryset=TestStep.objects.filter(test__id=self.kwargs.get('id')), prefix='steps'),
                form_postcondition_formset = self.form_postcondition_formset(queryset=TestPostcondition.objects.filter(test__id=self.kwargs.get('id')), prefix='postconditions')
            )


    def get_object(self):
        return Test.objects.filter(id=self.kwargs.get('id')).first()
