from typing import Any
from django.db import models
from django.shortcuts import render
from django.views.generic import DetailView
from .services import TestServices


class TestDetailView(DetailView):

    context_object_name = 'data'
    template_name = 'tests/test_detail.html'

    def get_object(self, queryset=None):
        test_id = self.kwargs.get('pk')
        data = TestServices.get_all_test_attributes(test_id)
        print(type(data))

        return data

    
    
        
    