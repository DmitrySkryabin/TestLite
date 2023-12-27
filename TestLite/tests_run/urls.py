from django.urls import path, include
from . import views
from .api import api

app_name = 'tests_run'

views_urls = [
    path('', views.TestRunListView.as_view(), name='test_run_list'),
    path('execute/<int:id>', views.TestRunCreateView.as_view(), name='execute'),
    path('run/<int:id>', views.TestRunDetailView.as_view(), name='test_run_detail'),
    # два варианта как можно отобразить тест суит (в первый раз: создать отобразить) и во второй просто отобразить
    path('test_suite', views.TestSuiteRunView.as_view(), name='test_suite'),
    path('test_suite/<int:id>', views.TestSuiteRunView.as_view(), name='test_suite'),
]

api_urls_v1 = [
    path('sample_method', api.sample_method, name='api_sample_method')
]


urlpatterns = [
    path('', include(views_urls)),
    path('api/v1/', include(api_urls_v1))
]
