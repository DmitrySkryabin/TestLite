from django.urls import path
from . import views

app_name = 'tests_run'

urlpatterns = [
    path('test_run/create', views.TestCreateView.as_view(), name='test_create'),
    path('test_run/<int:id>', views.TestDetailView.as_view(), name='test_detail'),
    path('test/<int:id>/update', views.TestUpdateView.as_view(), name='test_update'),
    path('tests', views.TestListView.as_view(), name='test_list')
]

