from typing import Any, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .services import TestServices
from .forms import TestForm


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
    template_name = 'tests/test_form.html'
    form_class = TestForm

    def get_object(self):
        test_id = self.kwargs.get('id')
        data = TestServices.get_all_test_attributes(id=test_id)

        return data


    def form_valid(self, form):
        TestServices.save_test(form=form, request=self.request)
        return super().form_valid(form)



class TestCreateView(CreateView):

    template_name = 'tests/test_form.html'
    form_class = TestForm

    def form_valid(self, form):
        TestServices.save_test(form=form, request=self.request)
        return super().form_valid(form)



    
    
        
    