from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('test/create', views.TestCreateView.as_view(), name='test_create'),
    path('test/<int:id>', views.TestDetailView.as_view(), name='test_detail'),
    path('test/<int:id>/update', views.TestUpdateView.as_view(), name='test_update'),
    path('', views.TestListView.as_view(), name='test_list')
]

