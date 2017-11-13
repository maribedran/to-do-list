import json

from django.conf import settings
from django.test import Client
from django.urls import reverse
from model_mommy import mommy


class LoginRequiredTestCaseMixin(object):

    def set_up_client(self):
        self.client = Client()
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        self.client.force_login(self.user)

    def test_list_is_login_required(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(403, response.status_code)

    def test_detail_is_login_required(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(403, response.status_code)

    def test_delete_is_login_required(self):
        self.client.logout()
        response = self.client.delete(self.detail_url)
        self.assertEqual(403, response.status_code)

    def test_create_is_login_required(self):
        self.client.logout()
        response = self.client.post(self.list_url, {})
        self.assertEqual(403, response.status_code)

    def test_update_is_login_required(self):
        self.client.logout()
        response = self.client.put(self.detail_url, {})
        self.assertEqual(403, response.status_code)


class CRUDTestCaseMixin(object):

    def set_up_objects(self):
        self.instance = mommy.make(self.model_class)
        self.list_url = reverse(f'{self.url_base_name}-list')
        self.detail_url = reverse(
            f'{self.url_base_name}-detail',
            args=[self.instance.id]
        )
        self.data = self.serializer_class(instance=self.instance).data

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
        count = self.model_class.objects.count()
        self.client.delete(self.detail_url)
        self.assertEqual(count - 1, self.model_class.objects.count())

    def test_create_returns_201(self):
        response = self.client.post(self.list_url, self.post_data)
        self.assertEqual(201, response.status_code)

    def test_create_returns_new_instance_data(self):
        count = self.model_class.objects.count()
        response = self.client.post(self.list_url, self.post_data)
        self.assertEqual(count + 1, self.model_class.objects.count())
        new_instance = self.model_class.objects.last()
        expected_data = self.serializer_class(instance=new_instance).data
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
        updated_instance = self.model_class.objects.get(id=self.instance.id)
        expected_data = self.serializer_class(instance=updated_instance).data
        self.assertEqual(expected_data, response.json())
