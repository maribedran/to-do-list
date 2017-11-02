from rest_framework import viewsets

from core.models import Task, ToDoList
from core.serializers import ToDoListSerializer


class ToDoListViewSet(viewsets.ModelViewSet):
    queryset = ToDoList.objects.prefetch_related('tasks').all()
    serializer_class = ToDoListSerializer

