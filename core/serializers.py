from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Task, ToDoList
from core.use_cases import (
    create_to_do_list_use_case,
    update_to_do_list_use_case
)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'description', 'created_at', 'due_at', 'done_at')
        read_only_fields = ('id', 'created_at',)


class ToDoListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    assignee = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ToDoList
        fields = ('id', 'name', 'assignee', 'tasks', 'created_at', 'earlyest_task',)
        read_only_fields = ('id', 'created_at', 'earlyest_task', 'assignee',)
        depth = 2

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['assignee'] = user
        return create_to_do_list_use_case(validated_data)

    def update(self, instance, validated_data):
        return update_to_do_list_use_case(instance, validated_data)

