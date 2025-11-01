from django.urls import path
from django.views.generic import ListView
from common_data.models import Lesson  # ← добавлен импорт
from . import views


class LessonsListView(ListView):
    model = Lesson
    template_name = 'teacher/lessons.html'
    context_object_name = 'lessons'

app_name = 'teacher'

urlpatterns = [
    path("dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("lessons/", LessonsListView.as_view(), name="lessons"),
    path("lessons/<int:lesson_id>/", views.lesson_details, name="lesson_details"),
    path("lesson/create/", views.create_lesson, name="create_lesson"),
    path("lessons/<int:lesson_id>/set_grade/", views.set_grade, name="set_grade"),
    path("profile/", views.profile_view, name="profile"),
]