from django.contrib import admin
from .models import UserProfile, Student, Lesson, Grade, SchoolClass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_teacher', 'is_student')
    list_filter = ('is_teacher', 'is_student')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Grade)
admin.site.register(SchoolClass)