from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view_tasks/", views.view_tasks, name="view_tasks"),
    path("add_task/", views.add_task, name="add_task"),
    path("export/", views.export_tasks, name="export_tasks"),
    path("import/", views.import_tasks, name="import_tasks"),
    path("charts/", views.charts, name="charts"),
]
