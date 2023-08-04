from django.contrib import admin
from .models import Task, TaskName

# Register your models here.

admin.site.register(Task)  # TaskAdmin should be registered with Task
admin.site.register(TaskName)  # TaskAdmin should be registered with Task
