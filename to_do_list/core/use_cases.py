from core.models import Task, ToDoList


def create_to_do_list_use_case(data):
    data = data.copy()
    tasks_data = data.pop('tasks', [])
    to_do_list = ToDoList.objects.create(**data)
    for task_data in tasks_data:
        task_data['to_do_list'] = to_do_list
        Task.objects.create(**task_data)
    return to_do_list


def update_to_do_list_use_case(data):
    data = data.copy()
    tasks_data = data.pop('tasks', [])
    ToDoList.objects.filter(id=data['id']).update(**data)
    to_do_list = ToDoList.objects.get(id=data['id'])
    for task_data in tasks_data:
        task_data['to_do_list'] = to_do_list
        task_id = task_data.pop('id', None)
        Task.objects.update_or_create(id=task_id, defaults=task_data)
    return to_do_list
