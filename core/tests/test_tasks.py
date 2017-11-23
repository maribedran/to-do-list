from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from model_mommy import mommy

from core.models import ToDoList, Task
from core.tasks import send_daily_email


class EmailTaskTest(TestCase):

    def setUp(self):
        now = timezone.now()
        tomorrow = now + timedelta(days=1)
        self.user = mommy.make(get_user_model(), email='mail@mail.com')
        self.to_do_list = mommy.make(ToDoList, assignee=self.user)
        self.done_task = mommy.make(
            Task,
            to_do_list=self.to_do_list,
            description='Ter app lab codes',
            due_at=now,
            done_at=now
        )
        self.to_do_task = mommy.make(
            Task,
            description='Chegar em São Paulo',
            to_do_list=self.to_do_list,
            due_at=tomorrow,
            done_at=None
        )

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_task_calls_send_email(self):
        self.assertEqual(mail.outbox, [])
        send_daily_email(self.user.id)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        body = '''
You have completed 1 task today:

- Ter app lab codes

You have 1 task for tomorrow:

- Chegar em São Paulo
'''
        self.assertEqual('Your daily tasks', email.subject)
        self.assertEqual(body, email.body)
        self.assertEqual(['mail@mail.com'], email.to)
        self.assertEqual('labcodestodolist@gmail.com', email.from_email)