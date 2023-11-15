from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory, modelformset_factory
from django.views.generic import DetailView, TemplateView, CreateView, FormView

from tests.models import Test, TestPrecondition, TestPostcondition, TestStep
from .models import TestRun, ResultChoice, TestRunPrecondition, TestRunStep, TestRunPostcondition
from .forms import TestRunForm, SelectResultForm, SelectResultForm2



class TestRunFormView(FormView):
    form_class = TestRunForm
    template_name = 'tests_run/test_run_form.html'

    def __init__(self):
        self.TestPreconditionFormset = modelformset_factory(form=SelectResultForm, model=TestRunPrecondition, extra=0)        
        self.TestStepFormset = modelformset_factory(form=SelectResultForm, model=TestRunStep, extra=0)        
        self.TestPostconditionFormset = modelformset_factory(form=SelectResultForm, model=TestRunPostcondition, extra=0)

        self.TestPreconditionFormsetTest = modelformset_factory(form=SelectResultForm2, model=TestRunPrecondition, extra=0) 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        test_id = self.kwargs.get('id')

        # Инициируем формсеты для шагов теста
        # self.TestPreconditionFormset = modelformset_factory(form=SelectResultForm, model=TestRunPrecondition, extra=0)        
        # self.TestStepFormset = modelformset_factory(form=SelectResultForm, model=TestRunStep, extra=0)        
        # self.TestPostconditionFormset = modelformset_factory(form=SelectResultForm, model=TestRunPostcondition, extra=0)

        context['test_id'] = test_id
        # context['test_precondition_formset'] = self.TestPreconditionFormset(queryset=TestPrecondition.objects.filter(test__id=test_id), prefix='preconditions')
        context['test_step_formset'] = self.TestStepFormset(queryset=TestStep.objects.filter(test__id=test_id), prefix='steps')
        context['test_postcondition_formset'] = self.TestPostconditionFormset(queryset=TestPostcondition.objects.filter(test__id=test_id), prefix='postconditions')

        # self.TestPreconditionFormsetTest = modelformset_factory(form=SelectResultForm2, model=TestRunPrecondition, extra=0)   
        if self.request.POST:
            print('ITS POST ----------------------')
            context['test_precondition_formset_test'] = self.TestPreconditionFormsetTest(self.request.POST, prefix='preconditions')
            print(context['test_precondition_formset_test'])
        else:
            print('ITS GET----------------------------------------')
            context['test_precondition_formset_test'] = self.TestPreconditionFormsetTest(queryset=TestPrecondition.objects.filter(test__id=test_id), prefix='preconditions')
            print(context['test_precondition_formset_test'])

        return context
    

    def form_valid(self, form):
        # print(self.request.POST)
        # context = self.get_context_data()
        #print(self.request.POST)
        # if context['test_precondition_formset_test'].is_valid():
        if self.TestPreconditionFormsetTest(self.request.POST, prefix='preconditions').is_valid():
            return HttpResponse('rer')
        else:
            #print(f"ERRORS:{context['test_precondition_formset_test'].errors}")
            return self.render_to_response(self.get_context_data(form=form))