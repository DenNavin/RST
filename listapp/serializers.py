from rest_framework import serializers

from .models import Task, Tag, CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_name': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        customuser = CustomUser(
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        customuser.set_password(password)
        customuser.save()
        return customuser


class TagSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=70)
    #task_id = serializers.IntegerField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


class TaskSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=800)
    date = serializers.DateField()
    tags = TagSerializer(many=True, read_only=True)


class TaskFullSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=70, allow_blank=False)
    description = serializers.CharField(max_length=800)
    date = serializers.DateField()
    #user_id = serializers.IntegerField()
    tags = TagSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, task, validated_data):
        task.title = validated_data.get('title', task.title)
        task.description = validated_data.get('description', task.description)
        task.date = validated_data.get('date', task.date)
        task.user_id = validated_data.get('user_id', task.user_id)

        task.save()
        return task


class TaskForFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'date']


class TagForFilterSerializer(serializers.ModelSerializer):
    task = TaskForFilterSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['title', 'task']
