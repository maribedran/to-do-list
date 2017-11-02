from rest_framework import serializers

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'description', 'created_at', 'due_at', 'done_at')
        read_only_fields = ('id', 'created_at',)

