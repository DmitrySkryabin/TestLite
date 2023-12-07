from django.urls import path
from . import views

app_name = 'tests_run'

urlpatterns = [
    path('', views.TestRunListView.as_view(), name='test_run_list'),
    path('execute/<int:id>', views.TestRunCreateView.as_view(), name='execute'),
    path('run/<int:id>', views.TestRunDetailView.as_view(), name='test_run_detail'),
    # два варианта как можно отобразить тест суит (в первый раз: создать отобразить) и во второй просто отобразить
    path('test_suite', views.TestSuiteRunView.as_view(), name='test_suite'),
    path('test_suite/<int:id>', views.TestSuiteRunView.as_view(), name='test_suite'),
]

