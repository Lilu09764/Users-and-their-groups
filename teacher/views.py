
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LessonForm, GradeForm
from common_data.models import Lesson, Student, UserProfile, Grade


@login_required(login_url='/accounts/login/')
def teacher_dashboard(request):
    teacher_profile, created = UserProfile.objects.get_or_create(user=request.user)
    lessons = Lesson.objects.filter(teacher=teacher_profile)
    return render(request, 'teacher/dashboard.html', {'lessons': lessons})


@login_required(login_url='/accounts/login/')
def create_lesson(request):
    teacher_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = teacher_profile
            lesson.save()
            return redirect('teacher:teacher_dashboard')
    else:
        form = LessonForm()

    return render(request, 'teacher/create_lesson.html', {'form': form})


@login_required(login_url='/accounts/login/')
def lesson_details(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)


    if lesson.school_class:
        students_in_context = Student.objects.filter(school_class=lesson.school_class)
    elif lesson.study_group:
        students_in_context = lesson.study_group.students.all()
    else:
        students_in_context = Student.objects.none()

    grades = Grade.objects.filter(lesson=lesson)

    return render(request, "teacher/lesson_details.html", {
        "lesson": lesson,
        "students": students_in_context,
        "grades": grades
    })


@login_required(login_url='/accounts/login/')
def set_grade(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        form = GradeForm(request.POST, lesson=lesson)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.lesson = lesson
            grade.save()
            return redirect("teacher:lesson_details", lesson_id=lesson_id)
    else:
        form = GradeForm(lesson=lesson)

    return render(request, "teacher/set_grade.html", {
        "lesson": lesson,
        "form": form
    })


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'teacher/profile.html', {'profile': profile})