from django.test import TestCase
from model_mommy import mommy

from django.contrib.auth import get_user_model
from core.models import Task, ToDoList
from core.serializers import TaskSerializer, ToDoListSerializer
from helpers.test import LoginRequiredTestCaseMixin, CRUDTestCaseMixin


class ToDoListViewSetTest(TestCase, LoginRequiredTestCaseMixin, CRUDTestCaseMixin):
    model_class = ToDoList
    serializer_class = ToDoListSerializer
    url_base_name = 'core:to_do_list'

    def setUp(self):
        user = mommy.make(get_user_model())
        self.post_data = {
            'name': 'My new life project',
            'assignee': user.id,
            'tasks': []
        }
        self.set_up_client()
        self.set_up_objects()
