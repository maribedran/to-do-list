from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
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

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_serializer_returns_correct_data(self):
        to_do_list = mommy.make(ToDoList)
        task = mommy.make(Task, to_do_list=to_do_list)
        serializer = ToDoListSerializer(instance=to_do_list)
        data = serializer.data

        expected_data = {
            'id': to_do_list.id,
            'name': to_do_list.name,
            'created_at': to_do_list.created_at.strftime(DATETIME_FORMAT),
            'earlyest_task': None,
            'assignee': to_do_list.assignee.id,
            'tasks': [
                {
                    'id': task.id,
                    'description': task.description,
                    'created_at': task.created_at.strftime(DATETIME_FORMAT),
                    'due_at': None,
                    'done_at': None,
                },
            ],
        }
        self.assertEqual(expected_data, data)

    @patch('core.serializers.create_to_do_list_use_case')
    def test_serializer_calls_create_to_do_list_use_case_on_create_with_logged_user(self, mocked_use_case):
        data = {
            'name': 'Things I have to do',
            'tasks': [{'description': 'Do that'}]
        }
        request = Mock(user=self.user)
        serializer = ToDoListSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        data.update({'assignee': self.user})
        mocked_use_case.assert_called_once_with(data)

    @patch('core.serializers.update_to_do_list_use_case')
    def test_serializer_calls_update_to_do_list_use_case_on_update(self, mocked_use_case):
        data = {
            'name': 'Things I have to do',
            'tasks': [{'description': 'Do that'}]
        }
        request = Mock(user=self.user)
        instance = mommy.make(ToDoList)
        serializer = ToDoListSerializer(data=data, instance=instance, context={'request': request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        mocked_use_case.assert_called_once_with(instance, data)
