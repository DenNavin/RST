from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, Tag
from .serializers import (
    TaskSerializer,
    TaskFullSerializer,
    RegistrationSerializer,
    TagForFilterSerializer)


class TaskView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    serializer_class = TaskSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        task = Task(user=user)
        serializer = TaskFullSerializer(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
        return Response({"success": "'{}' created successfully".format(task_saved.title)})


class TaskViewByID(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.request.user
        task = get_object_or_404(Task.objects.filter(user=user), pk=pk)
        serializer = TaskFullSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.request.user
        task = get_object_or_404(Task.objects.filter(user=user), pk=pk)
        data = request.data.get('task')
        serializer = TaskFullSerializer(instance=task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()

        return Response({'success': f"task '{task_saved.title}' updated successfully"})

    def delete(self, request, pk):
        user = self.request.user
        task = get_object_or_404(Task.objects.filter(user=user), pk=pk)
        task.delete()

        return Response({'success': f"task '{pk}' deleted successfully"}, status=204)


class TagView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Tag.objects.filter(user=user)

    serializer_class = TagForFilterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']


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
            token = Token.objects.get(user=customuser).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)