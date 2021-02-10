from rest_framework import serializers

from .models import Task, Tag


class TagSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=70)
    task_id = serializers.IntegerField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


class TaskSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=800)
    date = serializers.DateField()


class TaskFullSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=70, allow_blank=False)
    description = serializers.CharField(max_length=800)
    date = serializers.DateField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, task, validated_data):
        task.title = validated_data.get('title', task.title)
        task.description = validated_data.get('description', task.description)
        task.date = validated_data.get('date', task.date)
        task.user_id = validated_data.get('user_id', task.user_id)

        task.save()
        return task




