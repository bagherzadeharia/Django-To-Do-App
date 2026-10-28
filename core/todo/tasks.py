from celery import shared_task

from todo.models import Task

@shared_task
def deleteCompletedTasks():
    tasks = Task.objects.filter(
        complete=True
    ).delete()
