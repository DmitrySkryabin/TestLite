import itertools
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, TemplateView, CreateView, FormView, TemplateView

from tests.models import Test, TestPrecondition, TestPostcondition, TestStep
from .models import ResultChoice, TestRun, ResultChoice, TestRunPrecondition, TestRunStep, TestRunPostcondition
from .forms import TestRunForm, TestResultsFormset



# class TestRunFormView(FormView):
#     form_class = TestRunForm
#     template_name = 'tests_run/test_run_form.html'


#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         test_id = self.kwargs.get('id')

#         test_preconditions = [{'action': item.action, 'expected_result': item.expected_result} for item in TestPrecondition.objects.filter(test__id=test_id)]
#         test_steps = [{'action': item.action, 'expected_result': item.expected_result} for item in TestStep.objects.filter(test__id=test_id)]
#         test_postconditions = [{'action': item.action, 'expected_result': item.expected_result} for item in TestPostcondition.objects.filter(test__id=test_id)]
  
#         if self.request.POST:
#             context['test_precondition_formset'] = TestResultsFormset(self.request.POST, prefix='precondition')
#             context['test_step_formset'] = TestResultsFormset(self.request.POST, prefix='step', form_kwargs={'result_required': True})
#             context['test_postcondition_formset'] = TestResultsFormset(self.request.POST, prefix='postcondition')
#         else:
#             context['test_precondition_formset'] = TestResultsFormset(initial=test_preconditions, prefix='precondition')
#             context['test_step_formset'] = TestResultsFormset(initial=test_steps, prefix='step', form_kwargs={'result_required': True})
#             context['test_postcondition_formset'] = TestResultsFormset(initial=test_postconditions, prefix='postcondition')

#         context['test_id'] = test_id

#         return context
    
    
#     def fill_instance_of_data(self, instance, position, obj):
#         record = obj()
#         record.action = instance['action']
#         record.expected_result = instance['expected_result']
#         record.position = position

#         if instance['result'] == '':
#             record.result = 'P'
#         else:
#             record.result = instance['result']

#         return record


#     def form_valid(self, form):
#         context = self.get_context_data()
#         if context['test_precondition_formset'].is_valid() and context['test_step_formset'].is_valid() and context['test_postcondition_formset'].is_valid():
            
#             # тут нахуй убрать результат и тип пусть автоматом хуярит
#             # да и юзера нада ловить
            
#             test_run = form.save(commit=False)
#             test_run.test = Test.objects.get(id=context['test_id'])
#             test_run.start_on = datetime.now()
#             test_run.save()



#             for i, instance in enumerate(context['test_precondition_formset'].cleaned_data):
#                 test_run_precondition = self.fill_instance_of_data(instance, i, TestRunPrecondition)
#                 test_run_precondition.test_run = test_run
#                 test_run_precondition.save()
#             for i, instance in enumerate(context['test_step_formset'].cleaned_data):
#                 test_run_step = self.fill_instance_of_data(instance, i, TestRunStep)
#                 test_run_step.test_run = test_run
#                 test_run_step.save()
#             for i, instance in enumerate(context['test_postcondition_formset'].cleaned_data):
#                 test_run_postcondition = self.fill_instance_of_data(instance, i, TestRunPostcondition)
#                 test_run_postcondition.test_run = test_run
#                 test_run_postcondition.save()

#             return HttpResponse('heh')
#         else:
#             return self.render_to_response(self.get_context_data(form=form))

class TestRunFormView(TemplateView):
    template_name = 'tests_run/test_run_form.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        test_id = self.kwargs.get('id')

        test_preconditions = [{'action': item.action, 'expected_result': item.expected_result} for item in TestPrecondition.objects.filter(test__id=test_id)]
        test_steps = [{'action': item.action, 'expected_result': item.expected_result} for item in TestStep.objects.filter(test__id=test_id)]
        test_postconditions = [{'action': item.action, 'expected_result': item.expected_result} for item in TestPostcondition.objects.filter(test__id=test_id)]
  
        if self.request.POST:
            context['test_precondition_formset'] = TestResultsFormset(self.request.POST, prefix='precondition')
            context['test_step_formset'] = TestResultsFormset(self.request.POST, prefix='step', form_kwargs={'result_required': True})
            context['test_postcondition_formset'] = TestResultsFormset(self.request.POST, prefix='postcondition')
        else:
            context['test_precondition_formset'] = TestResultsFormset(initial=test_preconditions, prefix='precondition')
            context['test_step_formset'] = TestResultsFormset(initial=test_steps, prefix='step', form_kwargs={'result_required': True})
            context['test_postcondition_formset'] = TestResultsFormset(initial=test_postconditions, prefix='postcondition')

        context['test_id'] = test_id

        return context
    
    
    def fill_instance_of_data(self, instance, position, obj):
        record = obj()
        record.action = instance['action']
        record.expected_result = instance['expected_result']
        record.position = position

        if instance['result'] == '':
            record.result = 'P'
        else:
            record.result = instance['result']

        return record
    

    def assign_result_of_test_run(self, result):
        result = result


    def post(self, requset, *args, **kwargs):
        context = self.get_context_data()
        if context['test_precondition_formset'].is_valid() and context['test_step_formset'].is_valid() and context['test_postcondition_formset'].is_valid():
            
            # тут нахуй убрать результат и тип пусть автоматом хуярит
            # да и юзера нада ловить
            
            test_run = TestRun()
            test_run.test = Test.objects.get(id=context['test_id'])
            test_run.start_on = datetime.now()
            test_run.type = 'M'
            #test_run.save()

            calculated_result = ResultChoice.PASSED

            test_run_preconditions = []
            test_run_steps = []
            test_run_postconditions = []

            for i, instance in enumerate(context['test_precondition_formset'].cleaned_data):
                test_run_precondition = self.fill_instance_of_data(instance, i, TestRunPrecondition)
                test_run_precondition.test_run = test_run
                test_run_preconditions.append(test_run_precondition)

            for i, instance in enumerate(context['test_step_formset'].cleaned_data):
                test_run_step = self.fill_instance_of_data(instance, i, TestRunStep)
                test_run_step.test_run = test_run
                test_run_steps.append(test_run_step)

                print(f'1s:{type(test_run_step.result)}')
                print(f'2E:{type(calculated_result)}')
                if test_run_step.result > calculated_result:
                    #print(f'HEHEHEHEHHE:{test_run_step.result}')
                    calculated_result = test_run_step.result

            for i, instance in enumerate(context['test_postcondition_formset'].cleaned_data):
                test_run_postcondition = self.fill_instance_of_data(instance, i, TestRunPostcondition)
                test_run_postcondition.test_run = test_run
                test_run_postconditions.append(test_run_postcondition)

            test_run.result = calculated_result
            test_run.tester = requset.user
            test_run.save()

            for precondition, step, postcondition in itertools.zip_longest(test_run_preconditions, test_run_steps, test_run_postconditions):
                if precondition is not None:
                    precondition.save()
                if step is not None:
                    step.save()
                if postcondition is not None:
                    postcondition.save()

            return HttpResponse('heh')
        else:
            return self.render_to_response(self.get_context_data())