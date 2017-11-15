from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import Truncator


class ToDoList(models.Model):

    name = models.CharField(_('Name'), max_length=255)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('Assignee')
    )

    def __str__(self, *args, **kwargs):
        return self.name

    class Meta:
        verbose_name = _('To-Do List')

    @property
    def earlyest_task(self):
        return self.tasks.values_list('due_at', flat=True).earliest('due_at')


class Task(models.Model):
    description = models.CharField(_('Description'), max_length=255)
    to_do_list = models.ForeignKey(verbose_name=_('To-Do List'), to=ToDoList, related_name='tasks')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    due_at = models.DateTimeField(_('Due at'), null=True, blank=True)
    done_at = models.DateTimeField(_('Done at'), null=True, blank=True)

    def __str__(self, *args, **kwargs):
        return Truncator(self.description).chars(70)

    class Meta:
        verbose_name = _('Task')

