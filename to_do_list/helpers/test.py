from django.test import Client
from django.conf import settings
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
