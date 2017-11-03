from django.test import TestCase
from model_mommy import mommy

from core.models import Task, ToDoList
from core.use_cases import create_to_do_list_use_case, update_to_do_list_use_case


class CreateToDoListUseCaseTest(TestCase):

    def test_create_empty_to_do_list(self):
        data = {
            'name': 'My empty list',
        }
        count = ToDoList.objects.count()

        to_do_list = create_to_do_list_use_case(data)

        self.assertEqual(data['name'], to_do_list.name)
        self.assertEqual(count + 1, ToDoList.objects.count())

    def test_create_to_do_list_with_tasks(self):
        data = {
            'name': 'My tasks list',
            'tasks': [
                {
                    'description': 'Do something!'
                }
            ]
        }
        lists_count = ToDoList.objects.count()
        tasks_count = Task.objects.count()

        to_do_list = create_to_do_list_use_case(data)

        self.assertEqual(lists_count + 1, ToDoList.objects.count())
        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count + 1, Task.objects.count())
        self.assertEqual(1, to_do_list.tasks.count())
        new_task = to_do_list.tasks.first()
        self.assertEqual(data['tasks'][0]['description'], new_task.description)


class UpdateToDoListUseCaseTest(TestCase):

    def test_update_empty_to_do_list(self):
        list = mommy.make(ToDoList)
        data = {
            'id': list.id,
            'name': 'My empty list',
        }

        updated_list = update_to_do_list_use_case(data)

        self.assertEqual(list, updated_list)
        self.assertEqual(data['name'], updated_list.name)

    def test_update_to_do_list_adding_track(self):
        list = mommy.make(ToDoList)
        data = {
            'id': list.id,
            'name': 'My tasks list',
            'tasks': [
                {
                    'description': 'Do something!'
                }
            ]
        }
        tasks_count = Task.objects.count()

        to_do_list = update_to_do_list_use_case(data)

        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count + 1, Task.objects.count())
        self.assertEqual(1, to_do_list.tasks.count())
        new_task = to_do_list.tasks.first()
        self.assertEqual(data['tasks'][0]['description'], new_task.description)
