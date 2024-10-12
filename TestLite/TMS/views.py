import json
import datetime
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, View, CreateView
from django.forms import BaseModelForm, modelformset_factory
from .models import Project, TestCase, TestStep, TestSuite, TestSuiteRun, TestStepRun, TestCaseRun, TestCaseFolder
from .models import STATUS, PRIORITY, TYPE
from .forms import TestStepForm, TestCaseForm, TestSuiteForm, TestStepRunForm, TestStepRunFormset, TestCaseFormset
from .service import TestSuiteSaveHelper

# Create your views here.


class ProjectListView(ListView):
    model = Project


class TestCaseListView(ListView):

    def get_queryset(self) -> QuerySet[Any]:
        folder = self.request.GET.get('folder')
        if folder is not None:
            return TestCase.objects.filter(project__key=self.kwargs.get('project'), testcasefolder__id=folder)
        else:
            return TestCase.objects.filter(project__key=self.kwargs.get('project'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(key=self.kwargs.get('project'))
        for obj in context['object_list']:
            if TestCaseRun.objects.filter(test_case=obj).last() is not None:
                obj.status = TestCaseRun.objects.filter(test_case=obj).last().status
            else:
                obj.status = None
        context['testcase_folders'] = TestCaseFolder.objects.filter(project=context['project'])
        return context
    

class TestCaseDetailView(DetailView):
    template_name = 'TMS/testcase_detail.html'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        obj = TestCase.objects.get(pk=self.kwargs.get('pk'))
        return obj
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['testcase_parameters_as_text'] = json.dumps(self.object.parameters)
        context['testcase_steps'] = TestStep.objects.filter(test_case=self.object)
        context['testcaseruns'] = TestCaseRun.objects.filter(test_case=self.object).order_by('-stop_time')
        return context


class TestCaseUpdateView(UpdateView):
    model = TestCase
    form_class = TestCaseForm
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        testcase_step_formset = modelformset_factory(form=TestStepForm, model=TestStep, formset=TestCaseFormset, extra=0, can_delete=True)
        if self.request.POST:
            context['testcase_step_formset'] = testcase_step_formset(self.request.POST)
        else:
            context['testcase_step_formset'] = testcase_step_formset(queryset=TestStep.objects.filter(test_case=self.object))
        context['testcase'] = self.get_object
        
        return context
    

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        if context['testcase_step_formset'].is_valid():
            testcase = form.save()
            for teststep in context['testcase_step_formset'].save(commit=False):
                teststep.test_case = testcase
                teststep.save()
        else:
            print(context['testcase_step_formset'].errors)

        return redirect(reverse('TMS:testcase_detail', kwargs={'project': f'{self.object.project.key}', 'pk': self.object.pk}))
    


class TestCaseCreateView(CreateView):
    model = TestCase
    form_class = TestCaseForm
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        testcase_step_formset = modelformset_factory(form=TestStepForm, model=TestStep, extra=0)
        if self.request.POST:
            context['testcase_step_formset'] = testcase_step_formset(self.request.POST)
        else:
            context['testcase_step_formset'] = testcase_step_formset(queryset=TestStep.objects.none())
        context['testcase'] = self.get_object
        
        return context
    

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        if context['testcase_step_formset'].is_valid():
            testcase = form.save(commit=False)
            testcase.version = 1
            testcase.author = self.request.user
            testcase.project = Project.objects.get(key=self.kwargs.get('project'))
            testcase.save()
            for teststep in context['testcase_step_formset'].save(commit=False):
                teststep.test_case = testcase
                teststep.save()
        else:
            print(context['testcase_step_formset'].errors)

        return redirect(reverse('TMS:testcase_detail', kwargs={'project': f'{testcase.project.key}', 'pk': testcase.pk}))
    


class TestSuiteListView(ListView):
    model = TestSuite



class TestSuiteDetailView(DetailView):
    model = TestSuite

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['testsuiteruns'] = TestSuiteRun.objects.filter(test_suite=self.object).order_by('-date_time')
        return context



class TestSuiteUpdateView(UpdateView):
    model = TestSuite
    form_class = TestSuiteForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        testsuite = form.save()
        return redirect(reverse('TMS:testsuite_detail', kwargs={'project':f'{testsuite.test_cases.first().project.key}', 'pk': testsuite.pk}))
    


class TestSuiteExecuteV1(TemplateView):
    template_name = 'TMS/testsuite_execute_v1.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        project = kwargs.get('project')
        testsuite_pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        testsuite = TestSuite.objects.get(pk=testsuite_pk)
        context['testcases'] = testsuite.test_cases.all()
        teststep_formset = modelformset_factory(form=TestStepRunForm, model=TestStepRun, formset=TestStepRunFormset)
        context['teststep_formsets'] = dict()
        for testcase in context['testcases']:
            context['teststep_formsets'].update({
                f'{testcase.name}': teststep_formset(queryset=testcase, prefix=f'teststep_formset_{testcase.pk}')
                })
        return context
    

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        teststep_formset = modelformset_factory(form=TestStepRunForm, model=TestStepRun, formset=TestStepRunFormset)
        created = False
        for testcase in context['testcases']:
            if not created:
                testsuiterun = TestSuiteRun()
                testsuiterun.test_suite = TestSuite.objects.get(pk=kwargs.get('pk'))
                testsuiterun.type = TYPE.MANUAL
                created = True
            teststep_formsets = teststep_formset(request.POST, prefix=f'teststep_formset_{testcase.pk}')
            if teststep_formsets.is_valid():
                action = ''
                expected_result = ''
                for key, value in teststep_formsets.data.items():   # iter on both keys and values
                    if 'action' in key:
                        action = value
                    if 'expected_result' in key:
                        expected_result = value
                testcaserun = TestCaseRun()
                testcaserun.start_time = timezone.now()
                testcaserun.stop_time = timezone.now()
                testcaserun.duration = 99999
                testcaserun.type = TYPE.MANUAL
                testcaserun.test_suite_run = testsuiterun
                testcaserun.test_case = TestStep.objects.get(action=action, expected_result=expected_result).test_case

                min_status = STATUS.PASSED

                teststepruns = teststep_formsets.save(commit=False)
                for teststeprun in teststepruns:
                    if STATUS.get_object(teststeprun.result).its_more_important(min_status):
                        min_status = STATUS.get_object(teststeprun.result)

                if testsuiterun.status == '':
                    testsuiterun.status = min_status
                elif not STATUS.get_object(testsuiterun.status).its_more_important(min_status):
                    testsuiterun.status = min_status

                testsuiterun.save()
                testcaserun.status = min_status
                testcaserun.save()
                for teststeprun in teststepruns:
                    teststeprun.test_case_run = testcaserun
                    teststeprun.save()

        return redirect(reverse('TMS:testsuite_detail', kwargs={'project': kwargs.get('project'), 'pk': kwargs.get('pk')}))
    


class TestSuiteExecuteV2(TemplateView):
    template_name = 'TMS/testsuite_execute_v2.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        testsuite_pk = kwargs.get('pk')
        testsuiterun_pk = kwargs.get('testsuiterun_pk')
        context = super().get_context_data(**kwargs)
        testsuite = TestSuite.objects.get(pk=testsuite_pk)
        context['testcases'] = testsuite.test_cases.all()
        if testsuiterun_pk is None:
            context['testsuiterun'] = TestSuiteRun.objects.last().pk + 1
        else:
            context['testsuiterun'] = testsuiterun_pk
        return context
    

    def get_testcase(self, *args, **kwargs):
        print(kwargs)
        testcase_pk = kwargs.get('testcase_pk')
        testsuiterun_pk = kwargs.get('testsuiterun_pk')
        teststepruns = TestStepRun.objects.filter(test_case_run__test_suite_run__pk=testsuiterun_pk, test_case_run__test_case__pk=testcase_pk)
        testcase = TestCase.objects.get(pk=testcase_pk)
        teststep_formset = modelformset_factory(form=TestStepRunForm, model=TestStepRun, formset=TestStepRunFormset)
        if teststepruns:
            form = teststep_formset(queryset=teststepruns, prefix=f'teststep_formset')
        else:  
            form = teststep_formset(queryset=testcase, prefix=f'teststep_formset')
        return HttpResponse(str(form))

    
    def save(request, *args, **kwargs):
        teststep_formset = modelformset_factory(form=TestStepRunForm, model=TestStepRun, formset=TestStepRunFormset)
        teststepruns = teststep_formset(request.POST, prefix=f'teststep_formset')
        if teststepruns.is_valid():
            '''Создаем тестсуитеран если его не существует или получаем его если есть'''
            testsuiterun = TestSuiteRun.objects.filter(pk=kwargs.get('testsuiterun_pk')).first()
            if testsuiterun is None:
                testsuiterun = TestSuiteRun()
                testsuiterun.type = TYPE.MANUAL
                testsuiterun.test_suite = TestSuite.objects.get(pk=kwargs.get('pk'))

            '''Создаем новый ТестКейсРан'''
            testcaserun = TestCaseRun()
            testcaserun.start_time = timezone.now()
            testcaserun.stop_time = timezone.now()
            testcaserun.duration = 99999
            testcaserun.type = TYPE.MANUAL
            testcaserun.test_suite_run = testsuiterun
            testcaserun.test_case = TestCase.objects.get(pk=kwargs.get('testcase_pk'))

            teststepruns = teststepruns.save(commit=False)

            min_status = STATUS.PASSED
            for teststeprun in teststepruns:
                if STATUS.get_object(teststeprun.result).its_more_important(min_status):
                    min_status = STATUS.get_object(teststeprun.result)

    
            if testsuiterun.status == '':
                testsuiterun.status = min_status
            elif not STATUS.get_object(testsuiterun.status).its_more_important(min_status):
                testsuiterun.status = min_status

            testsuiterun.save()
            testcaserun.status = min_status
            testcaserun.save()
            for teststeprun in teststepruns:
                teststeprun.test_case_run = testcaserun
                teststeprun.save()
        return HttpResponse('SUCCESS')
    

class TestSuiteExecuteV3(TemplateView):
    template_name = 'TMS/testsuite_execute_v3.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        testsuite_pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        testsuite = TestSuite.objects.get(pk=testsuite_pk)
        testcases = testsuite.test_cases.all()
        context['testcases'] = testcases

        return context
    

    def post(self, request, *args, **kwargs):
        print(kwargs)
        data = []
        for testcase, steps in dict(request.POST).items():
            if testcase != 'csrfmiddlewaretoken':
                step_number_with_error = None
                status = 'skip'
                for i, step in enumerate(steps, start=1):
                    if step != 'S':
                        if step == 'P' and status != 'fail' and status != 'error':
                            status = 'passed'
                        if step == 'F' and status != 'error':
                            status = 'fail'
                            step_number_with_error = i
                        if step == 'E':
                            status = 'error'
                            step_number_with_error = i  
                data.append({
                    'testcase_key': f'{testcase}',
                    'status': status,
                    'duration': 9999,
                    'report': None, #ok
                    'log': '',
                    'skipreason': None, #ok
                    'precondition_status': 'passed',
                    'postcondition_status': 'passed',
                    'step_number_with_error': step_number_with_error,
                    'startime_readable': f'{datetime.datetime.now()}',
                    'stoptime_readable': f'{datetime.datetime.now()}'
                })
        TestSuiteSaveHelper.save_test_suite_run(TestSuite.objects.get(pk=kwargs.get('pk')).key, data, type=TYPE.MANUAL)
        
        return redirect(reverse('TMS:testsuite_detail', kwargs={'project': kwargs.get('project'), 'pk': kwargs.get('pk')}))
    


class TestSuiteRunDetailView(DetailView):
    model = TestSuiteRun

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['testcaseruns'] = TestCaseRun.objects.filter(test_suite_run=self.object)
        return context
    

class API:

    pass


class APIv1(API):

    @csrf_exempt
    def save_testsuite(request, *args, **kwargs):
        testsuite_key = kwargs.get('testsuite')
        data = json.loads(request.body)
        TestSuiteSaveHelper.save_test_suite_run(testsuite_key, data)

        return HttpResponse('LOL')
