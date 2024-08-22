from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.forms import modelformset_factory
from .models import Project, TestCase, TestStep
from .forms import TestStepForm, TestCaseForm

# Create your views here.


class ProjectListView(ListView):
    model = Project


class TestCaseListView(ListView):

    def get_queryset(self) -> QuerySet[Any]:
        return TestCase.objects.filter(project__name=self.kwargs.get('project'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['project'] = self.kwargs.get('project')
        return context
    

class TestCaseDetailView(DetailView):
    template_name = 'TMS/testcase_detail.html'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        obj = TestCase.objects.get(pk=self.kwargs.get('pk'))
        return obj
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['testcase_steps'] = TestStep.objects.filter(test_case=self.object)
        return context


class TestCaseUpdateView(UpdateView):
    model = TestCase
    form_class = TestCaseForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        testcase_step_formset = modelformset_factory(form=TestStepForm, model=TestStep)
        context['testcase_step_formset'] = testcase_step_formset(queryset=TestStep.objects.filter(test_case=self.object))
        
        return context
