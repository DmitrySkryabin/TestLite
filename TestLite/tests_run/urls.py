from django.urls import path
from . import views

app_name = 'tests_run'

urlpatterns = [
    path('execute/<int:id>', views.TestRunFormView.as_view(), name='execute'),
]

