from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Task, Tag
from .serializers import TaskSerializer, TaskFullSerializer, TagSerializer, RegistrationSerializer


class TaskView(APIView):
    def get(self, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response({'tasks': serializer.data})

    def post(self, request):
        task = request.data.get('task')
        serializer = TaskFullSerializer(data=task)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
        return Response({"success": "'{}' created successfully".format(task_saved.title)})


class TaskViewByID(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        serializer = TaskFullSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        data = request.data.get('task')
        serializer = TaskSerializer(instance=task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()

        return Response({'success': f"task '{task_saved.title}' updated successfully"})

    def delete(self, request, pk):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        task.delete()

        return Response({'success': f"task '{pk}' deleted successfully"}, status=204)


class TagView(APIView):
    def get(self, request):
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response({'tags': serializer.data})


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid(raise_exception=True):
            customuser = serializer.save()
            data['response'] = 'successfully registered user'
            data['email'] = customuser.email
            data['username'] = customuser.username
        else:
            data = serializer.errors
        return Response(data)