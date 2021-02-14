from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import TaskViewByID, registration_view, TagView, TaskView, TaskCreateView

urlpatterns = [
    path('tasks', TaskView.as_view()),
    path('tasks/new', TaskCreateView.as_view()),
    path('tasks/<int:pk>', TaskViewByID.as_view()),
    path('tags', TagView.as_view()),
    path('register', registration_view, name='register'),
    path('login', obtain_auth_token, name='login')
]
