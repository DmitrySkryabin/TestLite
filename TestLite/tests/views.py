from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
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



class TestSaveUpdateMixin():

    def __init__(self):
        pass 



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



# class TestCreateView(CreateView):
#     '''Создание нового инстанса теста'''
#     template_name = 'tests/test_form.html'
#     form_class = TestForm
    

#     def get_context_data(self, **kwargs):
#         '''
#         Добавялем новые формы для связанных с тестом атрибутов
#         Шаги, предусловия и постусловия
#         '''
#         context = super().get_context_data(**kwargs)
#         context.update(
#             TestServices.get_tests_all_forms()
#         )
#         return context
    

#     def post(self, request):
#         if TestForm(request.POST).is_valid():
#             forms = TestServices.get_valid_tests_forms(request)
#             if forms is not None:
#                 return self.form_valid(forms)
#             else:
#                 return self.form_invalid(forms)
#         return self.form_invalid()
         

#     def form_invalid(self, forms):
#         return super().form_invalid(self.get_context_data())

    
#     def form_valid(self, form):
#         '''Сохрание теста и переопределение перенаправяления к созданному тесту'''
#         test = TestServices.save_test_and_test_atibutes(form=form, request=self.request)
#         print('__________________')
#         print(form)
#         print('__________________')
#         #super().form_valid(form)

#         return redirect(reverse('tests:test_detail', kwargs={'id': test.id}))


from .forms import TestPreconditionForm, TestStepForm, TestPostconditionForm
class TestCreateView(CreateView):

    template_name = 'tests/test_form.html'
    form_class = TestForm


    def get_context_data(self, **kwargs: Any):
        print('------------------GET CONTEXT DATA--------------------------')
        #context = super().get_context_data(**kwargs)
        context = {}
        if kwargs.get('test_form') is not None:
            context['form'] = kwargs.get('test_form')
        else:
            context['form'] = TestForm()
        if kwargs.get('form_precondition_formset') is not None:
            print('RELOAD')
            context['form_precondition_formset'] =  kwargs.get('form_precondition_formset')
        else:
            print('NEW')
            context['form_precondition_formset'] = TestPreconditionForm()
        if kwargs.get('form_step_formset') is not None:
            context['form_step_formset'] = kwargs.get('form_step_formset')
        else:
            context['form_step_formset'] = TestStepForm()
        if kwargs.get('form_postcondition_formset') is not None:
            context['form_postcondition_formset'] = kwargs.get('form_postcondition_formset')
        else:
            context['form_postcondition_formset'] = TestPostconditionForm()

        return context
    

    def post(self, request):
        print('------------------POST--------------------------')
        test_form = TestForm(request.POST)
        form_precondition_formset = TestPreconditionForm(request.POST)
        form_step_formset = TestStepForm(request.POST)
        form_postcondition_formset = TestPostconditionForm(request.POST)

        if test_form.is_valid() and form_precondition_formset.is_valid() and form_step_formset.is_valid() and form_postcondition_formset.is_valid():
            return self.form_valid(
                test_form=test_form,
                form_precondition_formset=form_precondition_formset,
                form_step_formset=form_step_formset,
                form_postcondition_formset=form_postcondition_formset
            )
        else:
            return self.form_invalid(
                test_form=test_form,
                form_precondition_formset=form_precondition_formset,
                form_step_formset=form_step_formset,
                form_postcondition_formset=form_postcondition_formset
            )
    

    def form_valid(self, test_form, form_precondition_formset, form_step_formset, form_postcondition_formset):
        print('------------------FORM VALID--------------------------')
        test = test_form.instance
        test.author = self.request.user
        test.save()
        test_precondtions = form_precondition_formset.save(commit=False)
        test_precondtions.test = test
        print(test_precondtions)
        # for instance in form_precondition_formset.save(commit=False):
        #     instance.save()
        # for instance in form_step_formset.save(commit=False):
        #     instance.save()
        # for instance in form_postcondition_formset.save(commit=False):
        #     instance.save()

        return redirect(reverse('tests:test_detail', kwargs={'id': test.id}))
    

    def form_invalid(self, test_form, form_precondition_formset, form_step_formset, form_postcondition_formset):
        print('------------------FORM INVALID--------------------------')
        return self.render_to_response(self.get_context_data(
            test_form=test_form,
            form_precondition_formset=form_precondition_formset,
            form_step_formset=form_step_formset,
            form_postcondition_formset=form_postcondition_formset
        ))