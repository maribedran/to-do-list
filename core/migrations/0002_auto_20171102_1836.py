# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-02 18:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('due_at', models.DateTimeField(blank=True, null=True, verbose_name='Due at')),
                ('done_at', models.DateTimeField(blank=True, null=True, verbose_name='Done at')),
            ],
            options={
                'verbose_name': 'Task',
            },
        ),
        migrations.AlterModelOptions(
            name='todolist',
            options={'verbose_name': 'To-Do List'},
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='task',
            name='to_do_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='core.ToDoList', verbose_name='To-Do List'),
        ),
    ]
