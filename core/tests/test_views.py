from django.test import TestCase

from core.models import Task, ToDoList
from core.serializers import TaskSerializer, ToDoListSerializer
from helpers.test import LoginRequiredTestCaseMixin, CRUDTestCaseMixin


class ToDoListViewSetTest(TestCase, LoginRequiredTestCaseMixin, CRUDTestCaseMixin):
    model_class = ToDoList
    serializer_class = ToDoListSerializer
    url_base_name = 'core:to_do_list'
    post_data = {
        'name': 'My new life project',
        'tasks': []
    }

    def setUp(self):
        self.set_up_client()
        self.set_up_objects()
