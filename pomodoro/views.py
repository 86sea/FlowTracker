# from django.http import HttpResponse
# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login


# # Create your views here.


# def index(request):
# return HttpResponse("hello")
import csv
import json
import datetime
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from .models import Task, TaskName
from collections import defaultdict


@login_required
def charts(request):
    tasks = Task.objects.filter(user=request.user)

    # Initialize a nested dictionary with defaultdict
    task_times = defaultdict(lambda: defaultdict(int))

    for task in tasks:
        task_hour = task.date.hour
        task_times[task.name.name][task_hour] += task.length / 60  # convert to hours

    # Create lists for task names and hours of the day
    task_names = list(task_times.keys())
    hours = list(range(24))

    # Create a list of cumulative hours for each task
    cumulative_hours = [[task_times[task][hour] for hour in hours] for task in task_names]

    # Plot
    fig, ax = plt.subplots()

    for i, task in enumerate(task_names):
        ax.plot(hours, cumulative_hours[i], label=task)

    # Formatting
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Cumulative Hours')
    ax.set_title('Cumulative hours spent on each task by time of day')
    ax.legend()

    plt.xticks(range(0, 24, 1))

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_string = base64.b64encode(buf.getvalue()).decode()
    # response = HttpResponse(buf, content_type='image/png')


    return image_string
    # return response
# @login_required
# def charts(request):
    # tasks = Task.objects.filter(user=request.user)

    # task_lengths = {}

    # for task in tasks:
        # if task.name.name in task_lengths:
            # task_lengths[task.name.name] += task.length
        # else:
            # task_lengths[task.name.name] = task.length

    # fig1, ax1 = plt.subplots()
    # ax1.pie(task_lengths.values(),
            # labels=task_lengths.keys(),
            # autopct='%1.1f%%',
            # )
    # buf = BytesIO()
    # plt.savefig(buf, format='png')
    # plt.close(fig1)
    # buf.seek(0)
    # response = HttpResponse(buf, content_type='image/png')
    # return response


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    task_names = TaskName.objects.filter(user=request.user)
    ongoing_task_data = None
    chart_image = charts(request)

    if request.method == "POST":
        task_name_str = request.POST.get('task_name')
        select_task_name_str = request.POST.get('select_task_name')
        task_length_str = request.POST.get('task_length')

        if task_name_str: # if task_name input is not empty
            existing_task_name = TaskName.objects.filter(
                    user=request.user, name=task_name_str
                    )
            if not existing_task_name: # If the task name doesn't exist, create it
                TaskName.objects.create(user=request.user, name=task_name_str)

        else: # if task_name input is empty, then use the selected task_name
            task_name_str = select_task_name_str

        # Get the TaskName instance with the provided name
        task_name = TaskName.objects.get(
                user=request.user, name=task_name_str
                )

        # Convert task_length_str to an integer
        task_length = int(task_length_str)

        # Create a new task
        Task.objects.create(
                user=request.user, name=task_name, length=task_length
                )
        last_task = tasks.order_by('-date').first()  # Get the most recent task
            # If less time has passed than the task length, the task is ongoing
        ongoing_task = last_task
        ongoing_task_data = {
            'date': ongoing_task.date.isoformat(),
            'name': ongoing_task.name.name,
            'length': ongoing_task.length,
        }

    tasks_data = list(Task.objects.filter(user=request.user).values(
        'name__name', 'length', 'date'))
    for task in tasks_data:
        task['date'] = task['date'].isoformat()  # Convert datetime to string

    return render(request, 'pomodoro/index.html', {
        'tasks': json.dumps(tasks_data),
        'task_names': task_names,
        'ongoing_task': json.dumps(ongoing_task_data),
        'chart_image': chart_image,
    })


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
