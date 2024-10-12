from django.urls import path
from . import views

app_name = 'TMS'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='projects'),
    path('<slug:project>/testcases', views.TestCaseListView.as_view(), name='testcases'),
    path('<slug:project>/testcase/<int:pk>', views.TestCaseDetailView.as_view(), name='testcase_detail'),
    path('<slug:project>/testcase/create', views.TestCaseCreateView.as_view(), name='testcase_create'),
    path('<slug:project>/testcase/<int:pk>/update', views.TestCaseUpdateView.as_view(), name='testcase_update'),
    path('<slug:project>/testsuites', views.TestSuiteListView.as_view(), name='testsuites'),
    path('<slug:project>/testsuite/<int:pk>', views.TestSuiteDetailView.as_view(), name='testsuite_detail'),
    path('<slug:project>/testsuite/<int:pk>/update', views.TestSuiteUpdateView.as_view(), name='testsuite_update'),
    path('<slug:project>/testsuite/<int:pk>/execute/v1', views.TestSuiteExecuteV1.as_view(), name='testsuite_execute_v1'),
    path('<slug:project>/testsuite/<int:pk>/execute/v2', views.TestSuiteExecuteV2.as_view(), name='testsuite_execute_v2'),
    path('<slug:project>/testsuite/<int:pk>/execute/v3', views.TestSuiteExecuteV3.as_view(), name='testsuite_execute_v3'),
    path('<slug:project>/testsuite/<int:testsuite_pk>/run/<int:pk>', views.TestSuiteRunDetailView.as_view(), name='testsuiterun_detail'),

    # TestSuiteExecuteV2 доп запросы
    path('<slug:project>/testsuite/<int:pk>/execute/v2/<int:testsuiterun_pk>', views.TestSuiteExecuteV2.as_view(), name='testsuite_execute_v2'),
    path('<slug:project>/testsuite/<int:pk>/execute/v2/<int:testsuiterun_pk>/testcase/<int:testcase_pk>', views.TestSuiteExecuteV2.get_testcase, name='testsuite_execute_v2_get_testcase'),
    path('<slug:project>/testsuite/<int:pk>/execute/v2/<int:testsuiterun_pk>/testcase/<int:testcase_pk>/save', views.TestSuiteExecuteV2.save, name='testsuite_execute_v2_post_testcase'),

]
