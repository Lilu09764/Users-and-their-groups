from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from common_data.models import Lesson, Grade, Student


@login_required(login_url='/accounts/login/')
def student_dashboard(request):

    try:

        student = Student.objects.get(user=request.user)
        school_class = student.school_class
        lessons = Lesson.objects.filter(school_class=school_class)
    except Student.DoesNotExist:
        lessons = Lesson.objects.none()
        school_class = None

    context = {
        "lessons": lessons,
        "school_class": school_class,
    }
    return render(request, "student/dashboard.html", context)


@login_required(login_url='/accounts/login/')
def profile_view(request):

    student = getattr(request.user, "student", None)
    return render(request, "student/profile.html", {"student": student})


@login_required(login_url='/accounts/login/')
def my_grades(request):

    try:
        student = Student.objects.get(user=request.user)
        grades = Grade.objects.filter(student=student)
    except Student.DoesNotExist:
        grades = Grade.objects.none()

    return render(request, "student/my_grades.html", {"grades": grades})


@login_required(login_url='/accounts/login/')
def lesson_details(request, lesson_id):

    lesson = get_object_or_404(Lesson, pk=lesson_id)

    try:
        student = Student.objects.get(user=request.user)
        grade = Grade.objects.filter(student=student, lesson=lesson).first()
    except Student.DoesNotExist:
        grade = None

    return render(request, "student/lesson_details.html", {"lesson": lesson, "grade": grade})
