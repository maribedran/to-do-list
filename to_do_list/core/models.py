from django.db import models
from django.utils.translation import ugettext as _


class ToDoList(models.Model):

    name = models.CharField(_('Name'), max_length=255)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self, *args, **kwargs):
        return self.name

    class Meta:
        verbose_name = _('To-Do List')

