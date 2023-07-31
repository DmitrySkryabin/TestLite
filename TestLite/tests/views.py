from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView
from .services import TestServices


class TestDetailView(DetailView):
    '''Отображение детальной информации по тесту'''
    context_object_name = 'data'
    template_name = 'tests/test_detail.html'

    def get_object(self, queryset=None):
        test_id = self.kwargs.get('pk')
        data = TestServices.get_all_test_attributes(test_id)
        print(type(data))

        return data
    


class TestListView(ListView):
    '''Список всех тестов'''
    queryset = TestServices.get_all_tests()



class TestUpdateView(UpdateView):
    pass

    
    
        
    