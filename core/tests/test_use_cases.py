from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy

from core.models import Task, ToDoList
from core.use_cases import create_to_do_list_use_case, update_to_do_list_use_case


class CreateToDoListUseCaseTest(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def test_create_empty_to_do_list(self):
        data = {
            'name': 'My empty list',
            'assignee': self.user,
        }
        count = ToDoList.objects.count()

        to_do_list = create_to_do_list_use_case(data)

        self.assertEqual(data['name'], to_do_list.name)
        self.assertEqual(count + 1, ToDoList.objects.count())

    def test_create_to_do_list_with_tasks(self):
        data = {
            'name': 'My tasks list',
            'assignee': self.user,
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

        updated_list = update_to_do_list_use_case(list, data)

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

        to_do_list = update_to_do_list_use_case(list, data)

        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count + 1, Task.objects.count())
        self.assertEqual(1, to_do_list.tasks.count())
        new_task = to_do_list.tasks.first()
        self.assertEqual(data['tasks'][0]['description'], new_task.description)

    def test_update_to_do_list_updating_track(self):
        list = mommy.make(ToDoList)
        task = mommy.make(Task, to_do_list=list)
        data = {
            'id': list.id,
            'name': 'My tasks list',
            'tasks': [
                {
                    'id': task.id,
                    'description': 'Do something!'
                }
            ]
        }
        tasks_count = Task.objects.count()

        to_do_list = update_to_do_list_use_case(list, data)

        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count, Task.objects.count())
        self.assertEqual(1, to_do_list.tasks.count())
        new_task = to_do_list.tasks.first()
        self.assertEqual(data['tasks'][0]['description'], new_task.description)

    def test_update_to_do_list_updatting_track_and_adding_other(self):
        list = mommy.make(ToDoList)
        task = mommy.make(Task, to_do_list=list)
        data = {
            'id': list.id,
            'name': 'My tasks list',
            'tasks': [
                {
                    'id': task.id,
                    'description': 'Do something!'
                },
                {
                    'description': 'Do something else!'
                },
            ]
        }
        tasks_count = Task.objects.count()

        to_do_list = update_to_do_list_use_case(list, data)

        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count + 1, Task.objects.count())
        self.assertEqual(2, to_do_list.tasks.count())
        old_task, new_task = to_do_list.tasks.order_by('id').all()
        self.assertEqual(task, old_task)
        self.assertEqual(data['tasks'][0]['description'], old_task.description)
        self.assertEqual(data['tasks'][1]['description'], new_task.description)

    def test_update_to_do_list_deleting_task(self):
        list = mommy.make(ToDoList)
        task = mommy.make(Task, to_do_list=list)
        data = {
            'id': list.id,
            'name': 'My tasks list',
            'tasks': []
        }
        tasks_count = Task.objects.count()

        to_do_list = update_to_do_list_use_case(list, data)

        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count - 1, Task.objects.count())
        self.assertEqual(0, to_do_list.tasks.count())

    def test_update_to_do_list_deletting_updatting_and_adding_tracks(self):
        list = mommy.make(ToDoList)
        task_to_update = mommy.make(Task, to_do_list=list)
        task_to_delete = mommy.make(Task, to_do_list=list)
        data = {
            'id': list.id,
            'name': 'My tasks list',
            'tasks': [
                {
                    'id': task_to_update.id,
                    'description': 'Do something!'
                },
                {
                    'description': 'Do something else!'
                },
            ]
        }
        tasks_count = Task.objects.count()

        to_do_list = update_to_do_list_use_case(list, data)

        self.assertEqual(data['name'], to_do_list.name)

        self.assertEqual(tasks_count, Task.objects.count())
        self.assertEqual(2, to_do_list.tasks.count())
        self.assertFalse(Task.objects.filter(id=task_to_delete.id))
        old_task, new_task = to_do_list.tasks.order_by('id').all()
        self.assertEqual(task_to_update, old_task)
        self.assertEqual(data['tasks'][0]['description'], old_task.description)
        self.assertEqual(data['tasks'][1]['description'], new_task.description)
