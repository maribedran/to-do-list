from core.models import Task, ToDoList


def create_to_do_list_use_case(data):
    data = data.copy()
    tasks_data = data.pop('tasks', [])
    to_do_list = ToDoList.objects.create(**data)
    for task_data in tasks_data:
        task_data['to_do_list'] = to_do_list
        Task.objects.create(**task_data)
    return to_do_list