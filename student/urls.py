from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('grades/', views.my_grades, name='my_grades'),
    path('lesson/<int:lesson_id>/', views.lesson_details, name='lesson_details'),
    path('profile/', views.profile_view, name='profile'),
]
