from django.test import TestCase

from core.models import Task, ToDoList
from core.use_cases import create_to_do_list_use_case


class CreateToDoListUseCaseTest(TestCase):

    def test_create_empty_to_do_list(self):
        data = {
            'name': 'My empty list',
        }
        count = ToDoList.objects.count()
        to_do_list = create_to_do_list_use_case(data)
        self.assertEqual(count + 1, ToDoList.objects.count())
        new_list = ToDoList.objects.last()
        self.assertEqual(data['name'], new_list.name)


