from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from common_data.views import login_handler, logout_handler, register_handler


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login/", login_handler, name="login"),
    path("logout/", logout_handler, name="logout"),
    path("register/", register_handler, name="register"),
    path("student/", include("student.urls", namespace="student")),
    path("teacher/", include("teacher.urls", namespace="teacher")),
]

