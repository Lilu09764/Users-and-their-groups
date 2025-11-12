from django.contrib import admin
from .models import UserProfile, Student, Lesson, Grade, SchoolClass, StudyGroup


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_teacher', 'is_student')
    list_filter = ('is_teacher', 'is_student')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_class', 'study_groups_list')
    list_filter = ('school_class',)
    search_fields = ('user__username', 'user__first_name')

    def study_groups_list(self, obj):
        return ", ".join(g.name for g in obj.study_groups.all())
    study_groups_list.short_description = "Study Groups"


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'students_count')
    list_filter = ('created_by',)
    search_fields = ('name', 'description')
    filter_horizontal = ('students',)

    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = "Students"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'date', 'teacher', 'school_class', 'study_group')
    list_filter = ('date', 'school_class', 'study_group', 'teacher')
    search_fields = ('title', 'subject')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score', 'date', 'group_context')
    list_filter = ('date', 'lesson__school_class', 'lesson__study_group')
    search_fields = ('student__user__username', 'lesson__subject')


admin.site.register(SchoolClass)