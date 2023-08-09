from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view_tasks/", views.view_tasks, name="view_tasks"),
    path("add_task/", views.add_task, name="add_task"),
    path("export/", views.export_tasks, name="export_tasks"),
    path("import/", views.import_tasks, name="import_tasks"),
    path("charts/", views.charts, name="charts"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="pomodoro/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="pomodoor/logout.html"), name="logout"),
]
