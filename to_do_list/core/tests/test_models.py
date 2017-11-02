from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from core.models import ToDoList


class ToDoListModelTest(TestCase):

    @freeze_time(timezone.now())
    def test_save_persists_all_fields(self):
        now = timezone.now()
        objects_count = ToDoList.objects.count()
        instance = ToDoList(name='Shopping List')

        self.assertIsNone(instance.created_at)

        instance.save()

        self.assertEqual(objects_count + 1, ToDoList.objects.count())
        saved_instance = ToDoList.objects.last()
        self.assertTrue(saved_instance.id)
        self.assertEqual('Shopping List', saved_instance.name)
        self.assertEqual(now, saved_instance.created_at)

