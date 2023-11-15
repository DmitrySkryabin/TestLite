from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory, modelformset_factory
from django.views.generic import DetailView, TemplateView, CreateView, FormView

from tests.models import Test, TestPrecondition, TestPostcondition, TestStep
from .models import TestRun, ResultChoice, TestRunPrecondition, TestRunStep, TestRunPostcondition
from .forms import TestRunForm, SelectResultForm, SelectResultForm2



# class TestRunFormView(FormView):
#     form_class = TestRunForm
#     template_name = 'tests_run/test_run_form.html'

#     def __init__(self):     
#         self.TestStepFormset = modelformset_factory(form=SelectResultForm, model=TestRunStep, extra=0)        
#         self.TestPostconditionFormset = modelformset_factory(form=SelectResultForm, model=TestRunPostcondition, extra=0)

#         self.TestPreconditionFormset = modelformset_factory(form=SelectResultForm2, model=TestRunPrecondition, extra=0) 

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         test_id = self.kwargs.get('id')

#         context['test_id'] = test_id
#         context['test_step_formset'] = self.TestStepFormset(queryset=TestStep.objects.filter(test__id=test_id), prefix='steps')
#         context['test_postcondition_formset'] = self.TestPostconditionFormset(queryset=TestPostcondition.objects.filter(test__id=test_id), prefix='postconditions')
  
#         if self.request.POST:
#             print('ITS POST ----------------------')
#             context['test_precondition_formset'] = self.TestPreconditionFormset(self.request.POST, prefix='preconditions')
#         else:
#             print('ITS GET----------------------------------------')
#             #context['test_precondition_formset'] = self.TestPreconditionFormset(queryset=TestPrecondition.objects.filter(test__id=test_id), prefix='preconditions')
#             context['test_precondition_formset'] = self.TestPreconditionFormset(queryset=TestRunPrecondition.objects.filter(test_run__test__id=test_id))

#         return context
    

#     def form_valid(self, form):

#         if self.TestPreconditionFormset(self.request.POST, prefix='preconditions').is_valid():
#             return HttpResponse('rer')
#         else:
#             print(self.TestPreconditionFormset(self.request.POST, prefix='preconditions').errors)
#             return self.render_to_response(self.get_context_data(form=form))


class TestRunFormView(FormView):
    form_class = TestRunForm
    template_name = 'tests_run/test_run_form.html'

    def __init__(self):     
        self.TestPreconditionFormset = formset_factory(SelectResultForm2, extra=0)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        test_id = self.kwargs.get('id')

        context['test_id'] = test_id
  
        if self.request.POST:
            context['test_precondition_formset'] = self.TestPreconditionFormset(self.request.POST, prefix='preconditions')
        else:
            print([{'action': item.action, 'expected_result': item.expected_result} for item in TestPrecondition.objects.filter(test__id=test_id)])
            context['test_precondition_formset'] = self.TestPreconditionFormset(initial=[
                {'action': item.action, 'expected_result': item.expected_result} for item in TestPrecondition.objects.filter(test__id=test_id)
            ])

        return context
    

    # def form_valid(self, form):

    #     if self.TestPreconditionFormset(self.request.POST, prefix='preconditions').is_valid():
    #         return HttpResponse('rer')
    #     else:
    #         print(self.TestPreconditionFormset(self.request.POST, prefix='preconditions').errors)
    #         return self.render_to_response(self.get_context_data(form=form))