from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TaskView, TaskViewByID, TagView

urlpatterns = [
    path('tasks', TaskView.as_view()),
    path('tasks/<int:pk>', TaskViewByID.as_view()),
    #path('tasks/new', TaskViewByID.as_view()),
    path('tags', TagView.as_view()),
]
