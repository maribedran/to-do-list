from rest_framework import serializers

from core.models import Task, ToDoList
from core.use_cases import create_to_do_list_use_case


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

    def create(self, validated_data):
        return create_to_do_list_use_case(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('tasks', None)
        return super().update(instance, validated_data)
