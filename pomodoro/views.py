# from django.http import HttpResponse
# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login


# # Create your views here.


# def index(request):
# return HttpResponse("hello")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, TaskName


@login_required
def view_tasks(request):
    # Get all tasks associated with the current user
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'pomodoro/tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_length = request.POST.get('task_length')

        # Check if the task name already exists, create it if it doesn't
        task_name_obj, created = TaskName.objects.get_or_create(
            user=request.user,
            name=task_name,
        )

        # Now create the task associated with the task name
        task = Task.objects.create(
            user=request.user,
            name=task_name_obj,
            length=task_length,
        )

        task.save()

    return render(request, 'pomodoro/add_task.html')
