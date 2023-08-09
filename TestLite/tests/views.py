from django.shortcuts import redirect
from django.urls import reverse
from django.forms import formset_factory
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .services import TestServices
from .forms import TestForm, TestPostconditionForm, TestPreconditionForm, TestStepForm


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



class TestUpdateView(UpdateView):
    '''Редактирование инстанса теста'''
    template_name = 'tests/test_form.html'
    form_class = TestForm

    def get_object(self):
        test_id = self.kwargs.get('id')
        self.data = TestServices.get_all_test_attributes(id=test_id)

        return self.data.test


    def get_context_data(self):
        context = super().get_context_data()
        context.update(
            TestServices.get_tests_all_forms(self.data)
        )

        return context
        

    def form_valid(self, form):
        TestServices.save_test(form=form, request=self.request)
        return super().form_valid(form)



class TestCreateView(CreateView):
    '''Создание нового инстанса теста'''
    template_name = 'tests/test_form.html'
    form_class = TestForm
    

    def get_context_data(self):
        '''
        Добавялем новые формы для связанных с тестом атрибутов
        Шаги, предусловия и постусловия
        '''
        context = super().get_context_data()
        context.update(
            TestServices.get_tests_all_forms()
        )

        return context

    
    def form_valid(self, form):
        '''Сохрание теста и переопределение перенаправяления к созданному тесту'''
        test = TestServices.save_test(form=form, request=self.request)
        #super().form_valid(form)

        return redirect(reverse('tests:test_detail', kwargs={'id': test.id}))


    
    
        
    