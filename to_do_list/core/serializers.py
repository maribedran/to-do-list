from rest_framework import serializers

from core.models import Task, ToDoList


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'description', 'created_at', 'due_at', 'done_at')
        read_only_fields = ('id', 'created_at',)


class ToDoListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ('name', 'tasks')
        read_only_fields = ('id', 'created_at',)
        depth = 2
