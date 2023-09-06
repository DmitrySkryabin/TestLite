from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .services import TestServices
from .forms import TestForm
from .models import Test, TestPrecondition, TestStep, TestPostcondition
from .views_mixins import TestCreateUpdateMixin



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



class TestCreateView(TestCreateUpdateMixin ,CreateView):
    '''Создание теста и его атрибутов'''
    model=Test
    form_class=TestForm



class TestUpdateView(TestCreateUpdateMixin, UpdateView):
    '''Редактирование теста и его атрибутов'''
    model = Test
    form_class = TestForm


    def _set_formsets(self):
        '''
        Переопределяем логику отображения формсетов атрибутов класса
        чтобы при редактировании были указаны уже имеющиеся данные
        '''
        self._formsets = self.Formsets(
            form_precondition_formset = self.form_precondition_formset(queryset=TestPrecondition.objects.filter(test__id=self.kwargs.get('id')), prefix='preconditions'),
            form_step_formset = self.form_step_formset(queryset=TestStep.objects.filter(test__id=self.kwargs.get('id')), prefix='steps'),
            form_postcondition_formset = self.form_postcondition_formset(queryset=TestPostcondition.objects.filter(test__id=self.kwargs.get('id')), prefix='postconditions')
        )


    def get_object(self):
        return Test.objects.filter(id=self.kwargs.get('id')).first()
