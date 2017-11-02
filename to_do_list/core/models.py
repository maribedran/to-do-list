from django.db import models


class ToDoList(models.Model):

    name = models.CharField(max_length=255)
