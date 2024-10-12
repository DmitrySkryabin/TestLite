from django.urls import path
from . import views

app_name = 'TMS_API'

urlpatterns = [
    # Сохранение прогона теста из запроса
    path('v1/project/<slug:project>/testsuite/<slug:testsuite>/save', views.APIv1.save_testsuite, name='testsuite_save')
]
