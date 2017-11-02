import json
from django.test import TestCase, Client
from django.urls import reverse
from model_mommy import mommy

from core.models import Task, ToDoList
from core.serializers import TaskSerializer, ToDoListSerializer


class ToDoListViewSetTest(TestCase):

    def setUp(self):
        self.to_do_list = mommy.make(ToDoList)
        self.list_url = reverse('to_do_list-list')
        self.detail_url = reverse(
            'to_do_list-detail',
            args=[self.to_do_list.id]
        )
        self.data = ToDoListSerializer(instance=self.to_do_list).data
        self.client = Client()
        self.post_data = {
            'name': 'My new life project',
        }

    def test_list_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)

    def test_list_returns_correct_content(self):
        response = self.client.get(self.list_url)
        self.assertEqual([self.data], response.json())

    def test_detail_returns_200(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(200, response.status_code)

    def test_detail_returns_correct_content(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(self.data, response.json())

    def test_delete_returns_204(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(204, response.status_code)

    def test_delete_removes_entry_from_db(self):
        count = ToDoList.objects.count()
        self.client.delete(self.detail_url)
        self.assertEqual(count - 1, ToDoList.objects.count())

    def test_create_returns_201(self):
        response = self.client.post(self.list_url, self.post_data)
        self.assertEqual(201, response.status_code)

    def test_create_returns_new_instance_data(self):
        count = ToDoList.objects.count()
        response = self.client.post(self.list_url, self.post_data)
        self.assertEqual(count + 1, ToDoList.objects.count())
        new_instance = ToDoList.objects.last()
        expected_data = ToDoListSerializer(instance=new_instance).data
        self.assertEqual(expected_data, response.json())

    def test_update_returns_200(self):
        response = self.client.put(
            self.detail_url,
            json.dumps(self.post_data),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

    def test_update_returns_updated_instance_data(self):
        response = self.client.put(
            self.detail_url,
            json.dumps(self.post_data),
            content_type='application/json'
        )
        updated_instance = ToDoList.objects.get(id=self.to_do_list.id)
        expected_data = ToDoListSerializer(instance=updated_instance).data
        self.assertEqual(expected_data, response.json())
