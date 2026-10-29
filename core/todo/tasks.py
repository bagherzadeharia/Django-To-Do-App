import logging
from celery import shared_task

from todo.models import Task

logger = logging.getLogger(__name__)

@shared_task
def deleteCompletedTasks():
    deleted_count, _ = Task.objects.filter(complete=True).delete()
    if deleted_count:
        logger.info("%s Completed Tasks Have Been Deleted", deleted_count)
    else:
        logger.info("No Completed Task Has Been Deleted")
