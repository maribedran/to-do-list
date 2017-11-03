from core.models import Task, ToDoList


def create_to_do_list_use_case(data):
    to_do_list = ToDoList.objects.create(**data)
