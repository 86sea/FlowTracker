from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class TaskName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    name = models.ForeignKey(TaskName, on_delete=models.CASCADE)
    length = models.IntegerField(default=25)
    date = models.DateTimeField("Date", default=timezone.now)


    def __str__(self):
        return str(self.name)
