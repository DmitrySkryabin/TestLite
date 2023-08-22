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



# class TestUpdateView(UpdateView):
#     '''Редактирование инстанса теста'''
#     template_name = 'tests/test_form.html'
#     form_class = TestForm

#     def get_object(self):
#         test_id = self.kwargs.get('id')
#         self.data = TestServices.get_all_test_attributes(id=test_id)

#         return self.data.test


#     def get_context_data(self):
#         context = super().get_context_data()
#         context.update(
#             TestServices.get_tests_all_forms(self.data)
#         )

#         return context
        

#     def form_valid(self, form):
#         TestServices.save_test(form=form, request=self.request)
#         return super().form_valid(form)



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


# from .forms import TestPreconditionForm, TestStepForm, TestPostconditionForm
# from .models import Test, TestPrecondition, TestStep, TestPostcondition
# from django.forms import modelformset_factory
# class TestCreateView(CreateView):

#     template_name = 'tests/test_form.html'
#     form_class = TestForm


#     def __init__(self):
#         self.form_precondition_formset = modelformset_factory(model=TestPrecondition, form=TestPreconditionForm)
#         self.form_step_formset = modelformset_factory(model=TestStep, form=TestStepForm)
#         self.form_postcondition_formset = modelformset_factory(model=TestPostcondition, form=TestPostconditionForm)


#     def get_context_data(self, **kwargs: Any):
#         print('------------------GET CONTEXT DATA--------------------------')
        
#         #context = super().get_context_data(**kwargs)
#         context = {}
#         if kwargs.get('test_form') is not None:
#             context['form'] = kwargs.get('test_form')
#         else:
#             context['form'] = TestForm()
#         if kwargs.get('form_precondition_formset') is not None:
#             print('RELOAD')
#             context['form_precondition_formset'] =  kwargs.get('form_precondition_formset')
#         else:
#             print('NEW')
             
#             context['form_precondition_formset'] = self.form_precondition_formset(queryset=TestPrecondition.objects.none())
#         if kwargs.get('form_step_formset') is not None:
#             context['form_step_formset'] = kwargs.get('form_step_formset')
#         else:
            
#             context['form_step_formset'] = self.form_step_formset(queryset=TestStep.objects.none())
#         if kwargs.get('form_postcondition_formset') is not None:
#             context['form_postcondition_formset'] = kwargs.get('form_postcondition_formset')
#         else:
            
#             context['form_postcondition_formset'] = self.form_postcondition_formset(queryset=TestPostcondition.objects.none())

#         return context
    

#     def post(self, request):
#         print('------------------POST--------------------------')
#         test_form = TestForm(request.POST)
#         form_precondition_formset = self.form_precondition_formset(request.POST)
#         form_step_formset = self.form_step_formset(request.POST)
#         form_postcondition_formset = self.form_postcondition_formset(request.POST)

#         if test_form.is_valid() and form_precondition_formset.is_valid() and form_step_formset.is_valid() and form_postcondition_formset.is_valid():
#             return self.form_valid(
#                 test_form=test_form,
#                 form_precondition_formset=form_precondition_formset,
#                 form_step_formset=form_step_formset,
#                 form_postcondition_formset=form_postcondition_formset
#             )
#         else:
#             return self.form_invalid(
#                 test_form=test_form,
#                 form_precondition_formset=form_precondition_formset,
#                 form_step_formset=form_step_formset,
#                 form_postcondition_formset=form_postcondition_formset
#             )
    

#     def form_valid(self, test_form, form_precondition_formset, form_step_formset, form_postcondition_formset):
#         print('------------------FORM VALID--------------------------')
#         test = test_form.instance
#         test.author = self.request.user
#         test.save()
#         test_precondtions = form_precondition_formset.save(commit=False)
#         #test_precondtions.test = test
#         for item in test_precondtions:
#             print(item)
#         # for instance in form_precondition_formset.save(commit=False):
#         #     instance.save()
#         # for instance in form_step_formset.save(commit=False):
#         #     instance.save()
#         # for instance in form_postcondition_formset.save(commit=False):
#         #     instance.save()

#         return redirect(reverse('tests:test_detail', kwargs={'id': test.id}))
    

#     def form_invalid(self, test_form, form_precondition_formset, form_step_formset, form_postcondition_formset):
#         print('------------------FORM INVALID--------------------------')
#         return self.render_to_response(self.get_context_data(
#             test_form=test_form,
#             form_precondition_formset=form_precondition_formset,
#             form_step_formset=form_step_formset,
#             form_postcondition_formset=form_postcondition_formset
#         ))


from .forms import TestPreconditionForm, TestStepForm, TestPostconditionForm
from .models import Test, TestPrecondition, TestStep, TestPostcondition
from django.forms import modelformset_factory
class TestCreateView(CreateView):

    model=Test
    form_class=TestForm

    def get_context_data(self, **kwargs):
        print('==========GET CONTEXT DATA============')
        context = super().get_context_data(**kwargs)
        form_precondition_formset = modelformset_factory(form=TestPreconditionForm, model=TestPrecondition)
        form_step_formset = modelformset_factory(form=TestStepForm, model=TestStep)
        form_postcondition_formset = modelformset_factory(form=TestPostconditionForm, model=TestPostcondition)

        if self.request.POST:
            print('----------POST--------------')
            context['form_precondition_formset'] = form_precondition_formset(self.request.POST, prefix='preconditions')
            context['form_step_formset'] = form_step_formset(self.request.POST, prefix='steps')
            context['form_postcondition_formset'] = form_postcondition_formset(self.request.POST, prefix='postconditions')
        else:
            print('-----------GET----------')
            context['form_precondition_formset'] = form_precondition_formset(queryset=TestPrecondition.objects.none(), prefix='preconditions')
            context['form_step_formset'] = form_step_formset(queryset=TestStep.objects.none(), prefix='steps')
            context['form_postcondition_formset'] = form_postcondition_formset(queryset=TestPostcondition.objects.none(), prefix='postconditions')

        print(context['form_precondition_formset'])                   
        print(context['form_step_formset'])
        print(context['form_postcondition_formset'])
        return context


    def form_valid(self, form):
        print('===========FORM VALID============')
        context = self.get_context_data()
        if form.is_valid():
            print('------FORM VALID------')
            if context['form_precondition_formset'].is_valid() and context['form_step_formset'].is_valid() and context['form_postcondition_formset'].is_valid():
                print('------FORMSETS IS VALID--------')
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
                print('--------FORMSET INVALID----------')
                print(context['form_precondition_formset'])                   
                print(context['form_step_formset'])
                print(context['form_postcondition_formset'])
                print('\n')
        else:
            print('------FORM INVALID-------')
        return self.render_to_response(self.get_context_data(form=form))


    # def form_invalid(self, form):
    #     print('=======FORM INVALID=======')
    #     return self.render_to_response(self.get_context_data(form=form))


class TestUpdateView(UpdateView):

    model = Test
    form_class = TestForm


    def get_context_data(self, **kwargs):
        print('==========GET CONTEXT DATA============')
        context = super().get_context_data(**kwargs)
        form_precondition_formset = modelformset_factory(form=TestPreconditionForm, model=TestPrecondition)
        form_step_formset = modelformset_factory(form=TestStepForm, model=TestStep)
        form_postcondition_formset = modelformset_factory(form=TestPostconditionForm, model=TestPostcondition)

        if self.request.POST:
            print('----------POST--------------')
            context['form_precondition_formset'] = form_precondition_formset(self.request.POST, prefix='preconditions')
            context['form_step_formset'] = form_step_formset(self.request.POST, prefix='steps')
            context['form_postcondition_formset'] = form_postcondition_formset(self.request.POST, prefix='postconditions')
        else:
            print('-----------GET----------')
            context['form_precondition_formset'] = form_precondition_formset(queryset=TestPrecondition.objects.filter(id=self.kwargs.get('id')), prefix='preconditions')
            context['form_step_formset'] = form_step_formset(queryset=TestStep.objects.filter(id=self.kwargs.get('id')), prefix='steps')
            context['form_postcondition_formset'] = form_postcondition_formset(queryset=TestPostcondition.objects.filter(id=self.kwargs.get('id')), prefix='postconditions')

        print(context['form_precondition_formset'])                   
        print(context['form_step_formset'])
        print(context['form_postcondition_formset'])
        return context


    def form_valid(self, form):
        print('===========FORM VALID============')
        context = self.get_context_data()
        if form.is_valid():
            print('------FORM VALID------')
            if context['form_precondition_formset'].is_valid() and context['form_step_formset'].is_valid() and context['form_postcondition_formset'].is_valid():
                print('------FORMSETS IS VALID--------')
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
                print('--------FORMSET INVALID----------')
                print(context['form_precondition_formset'])                   
                print(context['form_step_formset'])
                print(context['form_postcondition_formset'])
                print('\n')
        else:
            print('------FORM INVALID-------')
        return self.render_to_response(self.get_context_data(form=form))