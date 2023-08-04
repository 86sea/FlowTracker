# from django.http import HttpResponse
# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login


# # Create your views here.


# def index(request):
# return HttpResponse("hello")
import csv
import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Task, TaskName


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    task_names = TaskName.objects.filter(user=request.user)

    if request.method == "POST":
        task_name_str = request.POST.get('task_name')
        task_length_str = request.POST.get('task_length')

        # If only task name is provided, it is the 'add_task' functionality
        if task_name_str and not task_length_str:
            existing_task_name = TaskName.objects.filter(user=request.user, name=task_name_str)
            if not existing_task_name:
                # If the task name doesn't exist, create it
                TaskName.objects.create(user=request.user, name=task_name_str)

        # If both task name and length are provided, it is the 'create task' functionality
        elif task_name_str and task_length_str:
            # Get the TaskName instance with the provided name
            task_name = TaskName.objects.get(user=request.user, name=task_name_str)

            # Convert task_length_str to an integer
            task_length = int(task_length_str)

            # Create a new task
            Task.objects.create(user=request.user, name=task_name, length=task_length)

    return render(request, 'pomodoro/index.html', {'tasks': tasks, 'task_names': task_names})


@login_required
def view_tasks(request):
    # Get all tasks associated with the current user
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'pomodoro/tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == "POST":
        task_name = request.POST.get('task_name')

        # Check if the task name already exists for this user
        existing_task_name = TaskName.objects.filter(
                user=request.user, name=task_name
                )
        if not existing_task_name:
            # If it doesn't exist, create it
            TaskName.objects.create(
                user=request.user,
                name=task_name,
            )

    return render(request, 'pomodoro/add_task.html')


@login_required
def export_tasks(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    tasks = Task.objects.filter(user=request.user)

    for task in tasks:
        date_str = task.date.strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([task.name.name, task.length, date_str])
    return response


@login_required
def import_tasks(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)

        for row in reader:
            task_name_str, task_length_str, task_date_str = row

            task_name, _ = TaskName.objects.get_or_create(
                    user=request.user, name=task_name_str
                    )
            task_length = int(task_length_str)
            task_date = datetime.datetime.strptime(
                    task_date_str, '%Y-%m-%d %H:%M:%S'
                    )
            task_date = timezone.make_aware(task_date, timezone=timezone.utc)

            Task.objects.create(
                    user=request.user,
                    name=task_name,
                    length=task_length,
                    date=task_date
                    )
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'pomodoro/import.html')
