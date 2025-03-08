from django.urls import path
from .views import task_verification

urlpatterns = [
    path('task-verification/', task_verification, name='task_verification'),
]
