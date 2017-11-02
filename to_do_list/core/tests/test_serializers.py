from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from core.models import Task, ToDoList
from core.serializers import TaskSerializer, ToDoListSerializer

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class TaskSerializerTest(TestCase):
    max_diff = None

    def test_serializer_returns_correct_data(self):
        now = timezone.now()
        task = mommy.make(Task, due_at=now, done_at=now)

        serializer = TaskSerializer(instance=task)
        data = serializer.data
        expected_data = {
            'id': task.id,
            'description': task.description,
            'created_at': task.created_at.strftime(DATETIME_FORMAT),
            'due_at': task.due_at.strftime(DATETIME_FORMAT),
            'done_at': task.done_at.strftime(DATETIME_FORMAT),
        }

        self.assertEqual(expected_data, data)


class ToDoListSerializerTest(TestCase):

    def test_serializer_returns_correct_data(self):
        to_do_list = mommy.make(ToDoList)
        task = mommy.make(Task, to_do_list=to_do_list)
        serializer = ToDoListSerializer(instance=to_do_list)
        data = serializer.data

        expected_data = {
            'name': to_do_list.name,
            'created_at': to_do_list.created_at.strftime(DATETIME_FORMAT),
            'tasks': [
                {
                    'id': task.id,
                    'description': task.description,
                    'created_at': task.created_at.strftime(DATETIME_FORMAT),
                    'due_at': '',
                    'done_at': '',
                },
            ],
        }
