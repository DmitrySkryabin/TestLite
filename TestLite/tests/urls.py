from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('test/create', views.TestCreateView.as_view(), name='test_create'),
    path('test/<int:id>', views.TestDetailView.as_view(), name='test_detail'),
    path('test/<int:id>/update', views.TestUpdateView.as_view(), name='test_update'),
    path('test_plans', views.TestPlanListView.as_view(), name='test_plan_list'),
    path('test_plan/create', views.TestPlanCreateView.as_view(), name='test_plan_create'),
    path('test_plan/<int:test_plan_id>', views.TestPlanDetailView.as_view(), name='test_plan_detail'),
    path('test_plan/<int:test_plan_id>/update', views.TestPlanUpdateView.as_view(), name='test_plan_update'),
    path('', views.TestListView.as_view(), name='test_list')
]

