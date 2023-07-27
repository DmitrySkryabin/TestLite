from django.shortcuts import render
from django.views.generic import DetailView
from .services import TestServices



class TestDetailView(DetailView):

    context_object_name = 'test'

    def get_object(self, queryset=None):
        test_id = self.kwargs.get('pk')
        data = TestServices.get_all_test_attributes(test_id)

        return data

    