from django.urls import path
from . import views

app_name = 'TMS'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='projects'),
    path('<slug:project>/', views.TestCaseListView.as_view(), name='testcases'),
    path('<slug:project>/testcase/<int:id>', views.TestCaseDetailView.as_view(), name='testcase_detail'),
]
