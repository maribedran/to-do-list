from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from core.models import Task
from core.serializers import TaskSerializer

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
