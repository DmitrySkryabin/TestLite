from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, TemplateView, CreateView, FormView

from tests.models import Test, TestPrecondition, TestPostcondition, TestStep
from .models import TestRun, ResultChoice
from .forms import TestRunForm, SelectResultForm

# Create your views here.


class TestRunFormView(FormView):
    # Походу нужно побпловаться с формсет фактори
    form_class = TestRunForm
    template_name = 'tests_run/test_run_form.html'


    def get_context_data(self):
        context = super().get_context_data()
        test_id = self.kwargs.get('id')
        
        context['test_id'] = test_id
        context['select'] = SelectResultForm
        context['test_preconditions'] = TestPrecondition.objects.filter(test__id=test_id)
        context['test_steps'] = TestStep.objects.filter(test__id=test_id)
        context['test_postconditions'] = TestPostcondition.objects.filter(test__id=test_id)

        return context
    

    def form_valid(self, form):
        print('________________')
        print(self.request.POST['steps'])
        print(''.join(self.request.POST['steps']))
        print(TestStep.objects.filter(test__id=self.kwargs.get('id')).count())
        if len(''.join(self.request.POST['steps'])) == TestStep.objects.filter(test__id=self.kwargs.get('id')).count():
            print(self.request.POST['steps'])
        return HttpResponse('rer')