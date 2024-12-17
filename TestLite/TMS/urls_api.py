from django.urls import path
from . import views

app_name = 'TMS_API'

urlpatterns = [
    # Сохранение прогона теста из запроса
    path('v1/project/<slug:project>/testsuite/<slug:testsuite>/save', views.APIv1.save_testsuite, name='testsuite_save'),
    # Получение списка тесткейсов для тестсуита 
    path('v1/testsuite/<slug:testsuite>/get/testcases', views.APIv1.get_testcases_in_testsuite, name='get_testcases_in_testsuite'),
    # Получаем парметры для теста
    path('v1/testcase/<slug:testcase>/get/parameters', views.APIv1.get_testcase_parameters, name='get_testcase_parameters')
]
