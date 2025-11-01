from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Импортируем представления для аутентификации
from . import views


def home(request):
    return render(request, "home.html")

urlpatterns = [

    path("admin/", admin.site.urls),


    path("", views.home, name="index"),


    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),


    path("accounts/signup/", views.signup, name="signup"),


    path("register/", include("common_data.urls")),


    path("student/", include(("student.urls", "student"), namespace="student")),
    path("teacher/", include(("teacher.urls", "teacher"), namespace="teacher")),
]


