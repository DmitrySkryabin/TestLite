import itertools
import datetime
from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, CreateView, FormView, TemplateView, ListView

from tests.models import Test, TestPrecondition, TestPostcondition, TestStep
from .models import ResultChoice, TestRun, ResultChoice, TestRunPrecondition, TestRunStep, TestRunPostcondition, TestRunSuite
from .forms import TestRunForm, TestResultsFormset
from .services import TestRunServices


class TestRunListView(ListView):
    '''Список всех ранов (прогонов) теста'''
    # test_runs = TestRun.objects.all()
    # for test_run in test_runs:
    #     print(test_run)
    # queryset = TestRun.objects.all()
    
    def get_queryset(self):
        import json
        from django.core.serializers.json import DjangoJSONEncoder
        print(json.dumps(list(TestRun.objects.values()), cls=DjangoJSONEncoder))
        return TestRun.objects.all()
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        tests_run = []
        test_run_suite = None
        boofer = []
        for test_run in TestRun.objects.all():
            if test_run.test_run_suite is not None:
                boofer.append(test_run)
                if test_run_suite != test_run.test_run_suite:
                    tests_run.append(boofer)
                    test_run_suite = test_run.test_run_suite
                    boofer = []
            else:
                tests_run.append(test_run)
        context['testrun_list'] = tests_run

        return context



class TestRunDetailView(DetailView):
    '''Детальная информация по прогону теста'''
    context_object_name = 'data'
    template_name = 'tests_run/testrun_detail.html'

    def get_object(self):
        test_run = TestRun.objects.filter(id=self.kwargs.get('id')).first()
        test_run.duration = datetime.timedelta(seconds=int((test_run.stop_on - test_run.start_on).total_seconds()))
        return {
            'test_run':test_run,
            'test_run_preconditions': TestRunPrecondition.objects.filter(test_run__id=self.kwargs.get('id')).all(),
            'test_run_steps': TestRunStep.objects.filter(test_run__id=self.kwargs.get('id')).all(),
            'test_run_postconditions': TestRunPostcondition.objects.filter(test_run__id=self.kwargs.get('id')).all()
        }



class TestRunCreateView(TemplateView):
    '''Вью для сохранения экземпляра выполнения теста'''
    template_name = 'tests_run/testrun_form.html'


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

        context['test'] = Test.objects.filter(id=test_id).first()
        return context
    

    def get(self, request, id):
        '''Сохраняем время первого запуска при отркрытии страницы'''
        request.session['time'] = str(timezone.now())
        return super().get(request, id)


    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['test_precondition_formset'].is_valid() and context['test_step_formset'].is_valid() and context['test_postcondition_formset'].is_valid():
            
            test_run = TestRunServices.save_test_run(
                test=context['test'],
                user=request.user,
                start_time=request.session['time'],
                preconditions=context['test_precondition_formset'].cleaned_data,
                steps=context['test_step_formset'].cleaned_data,
                postconditions=context['test_postcondition_formset'].cleaned_data
            )

            return redirect(reverse('tests_run:test_run_detail', kwargs={'id': test_run.id}))
        else:
            return self.render_to_response(self.get_context_data())