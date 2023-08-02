"""
URL configuration for TestLite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('test/create', views.TestCreateView.as_view(), name='test_create'),
    path('test/<int:id>', views.TestDetailView.as_view(), name='test_detail'),
    path('test/<int:id>/update', views.TestUpdateView.as_view(), name='test_update'),
    path('tests', views.TestListView.as_view(), name='test_list')
]

