from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from model_mommy import mommy

from core.models import ToDoList, Task


class ToDoListModelTest(TestCase):

    @freeze_time(timezone.now())
    def test_save_persists_all_fields(self):
        now = timezone.now()
        objects_count = ToDoList.objects.count()
        user = mommy.make(get_user_model())
        instance = ToDoList(name='Shopping List', assignee=user)

        self.assertIsNone(instance.created_at)

        instance.save()

        self.assertEqual(objects_count + 1, ToDoList.objects.count())
        saved_instance = ToDoList.objects.last()
        self.assertTrue(saved_instance.id)
        self.assertEqual('Shopping List', saved_instance.name)
        self.assertEqual(now, saved_instance.created_at)
        self.assertEqual(user, saved_instance.assignee)

    def test_earlyest_task_property(self):
        now = timezone.now()
        tomorrow = now + timedelta(days=1)
        to_do_list = mommy.make(ToDoList)
        first_task = mommy.make(
            Task,
            to_do_list=to_do_list,
            due_at=now
        )
        first_task = mommy.make(
            Task,
            to_do_list=to_do_list,
            due_at=tomorrow
        )
        self.assertEqual(now, to_do_list.earlyest_task)

    def test_to_do_list_has_assignee_user(self):
        to_do_list = mommy.make(ToDoList)
        self.assertIsInstance(to_do_list.assignee, get_user_model())

class TaskModelTest(TestCase):

    @freeze_time(timezone.now())
    def test_save_persists_all_fields(self):
        now = timezone.now()
        objects_count = Task.objects.count()

        to_do_list = mommy.make(ToDoList)
        instance = Task(
            description='Buy beer',
            to_do_list=to_do_list,
            due_at=now,
            done_at=now
        )

        self.assertIsNone(instance.created_at)

        instance.save()

        self.assertEqual(objects_count + 1, Task.objects.count())
        saved_instance = Task.objects.last()
        self.assertTrue(saved_instance.id)
        self.assertEqual('Buy beer', saved_instance.description)
        self.assertEqual(now, saved_instance.created_at)
        self.assertEqual(now, saved_instance.due_at)
        self.assertEqual(now, saved_instance.done_at)

    def test_str_truncates_description(self):
        instance = Task(description='A' * 80, to_do_list=mommy.make(ToDoList))
        self.assertEqual('%s...' % ('A' * 67), str(instance))



