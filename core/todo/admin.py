from todo.models import Task
from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'complete',
    )
    fields = (
        'title',
        'user',
        'complete',
    )

admin.site.register(Task, TaskAdmin)