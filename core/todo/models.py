from django.db import models
from django.urls import reverse

class Task(models.Model):
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200, null=False, blank=False)
    complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_absolute_api_url(self):
        return reverse('todo:api-v1:task-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        order_with_respect_to = "user"