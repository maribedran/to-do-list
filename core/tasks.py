from datetime import date, timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from core.models import Task
from to_do_list.celery import app


@app.task
def send_daily_email(user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    today = date.today()
    tomorrow = today + timedelta(days=1)
    done_today = Task.objects.filter(
        done_at__date=today,
        to_do_list__assignee=user_id
    ).values_list('description', flat=True)
    to_do_tomorrow = Task.objects.filter(
        done_at__isnull=True,
        due_at__date=tomorrow,
        to_do_list__assignee=user_id
    ).values_list('description', flat=True)
    done_today_list = '\n'.join([f'- {description}' for description in done_today])
    to_do_tomorrow_list = '\n'.join([f'- {description}' for description in to_do_tomorrow])
    body = f'''
You have completed {done_today.count()} task today:

{done_today_list}

You have {to_do_tomorrow.count()} task for tomorrow:

{to_do_tomorrow_list}
'''
    send_mail('Your daily tasks', body, settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email])